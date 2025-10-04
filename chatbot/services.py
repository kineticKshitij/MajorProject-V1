from google import genai
from google.genai import types
from django.conf import settings
from django.core.cache import cache
import time
import logging
import json
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class GeminiChatService:
    """Service for interacting with Google Gemini API using the new google-genai package"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model_name = settings.GEMINI_MODEL
        self.system_prompt = settings.CHATBOT_SYSTEM_PROMPT
        self.max_history = settings.CHATBOT_MAX_HISTORY
        
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not configured. Chatbot will not function.")
            self.client = None
            return
        
        # Initialize the client with API key
        self.client = genai.Client(api_key=self.api_key)
    
    @classmethod
    def get_service_for_user(cls, user):
        """Get a GeminiChatService instance configured for a specific user"""
        if hasattr(user, 'gemini_api_key') and user.gemini_api_key:
            return cls(api_key=user.gemini_api_key)
        else:
            # Fall back to global API key
            return cls()
    
    def is_configured(self) -> bool:
        """Check if the service is properly configured"""
        return bool(self.api_key and self.client)
    
    def format_message_history(self, messages: List[Dict]) -> List[Dict]:
        """Format message history for Gemini API"""
        formatted_messages = []
        
        # Don't add system prompt here - it will be added as system_instruction
        # The Gemini API doesn't support "system" role in contents
        
        for msg in messages[-self.max_history:]:  # Limit history
            role = "user" if msg["message_type"] == "user" else "model"
            formatted_messages.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })
        
        return formatted_messages
    
    def get_dork_context(self, user_message: str) -> str:
        """Get relevant dork information based on user message"""
        # Import here to avoid circular imports
        from googledorks.models import GoogleDork, DorkCategory
        from django.db import models
        
        # Simple keyword matching for now - could be enhanced with embeddings
        keywords = user_message.lower().split()
        
        # Look for relevant dorks
        relevant_dorks = []
        for keyword in keywords:
            dorks = GoogleDork.objects.filter(
                models.Q(title__icontains=keyword) |
                models.Q(description__icontains=keyword) |
                models.Q(tags__icontains=keyword)
            ).select_related('category')[:3]
            relevant_dorks.extend(dorks)
        
        # Remove duplicates
        unique_dorks = list({dork.id: dork for dork in relevant_dorks}.values())[:5]
        
        if unique_dorks:
            context = "\n\nRelevant Google Dorks from our database:\n"
            for dork in unique_dorks:
                context += f"- **{dork.title}** ({dork.category.name}): {dork.query}\n"
                context += f"  Description: {dork.description[:100]}...\n"
                context += f"  Risk Level: {dork.get_risk_level_display()}\n\n"
            
            return context
        
        return ""
    
    def get_entity_context(self, user_message: str, user=None) -> str:
        """Get relevant entity information based on user message"""
        # Import here to avoid circular imports
        from googledorks.models import Entity, EntityType, EntitySearchTemplate
        from django.db import models
        
        # Extract keywords from user message
        keywords = user_message.lower().split()
        entity_keywords = ['company', 'person', 'organization', 'government', 'educational', 'domain', 'website']
        
        # Check if message mentions entities
        if not any(keyword in user_message.lower() for keyword in entity_keywords):
            return ""
        
        context = "\n\nEntity Research Context:\n"
        
        # Get recent entities for the user
        if user and hasattr(user, 'entity_set'):
            recent_entities = user.entity_set.order_by('-created_at')[:3]
            if recent_entities:
                context += "Your Recent Entities:\n"
                for entity in recent_entities:
                    context += f"- **{entity.name}** ({entity.entity_type.name})\n"
                    if entity.description:
                        context += f"  Description: {entity.description[:80]}...\n"
                context += "\n"
        
        # Look for relevant entity types
        relevant_types = EntityType.objects.filter(
            models.Q(name__icontains=' '.join(keywords)) |
            models.Q(description__icontains=' '.join(keywords))
        )[:3]
        
        if relevant_types:
            context += "Relevant Entity Types:\n"
            for entity_type in relevant_types:
                context += f"- **{entity_type.name}**: {entity_type.description}\n"
                
                # Get sample search templates for this type
                templates = EntitySearchTemplate.objects.filter(
                    entity_type=entity_type,
                    is_active=True
                )[:2]
                
                if templates:
                    context += "  Sample Search Templates:\n"
                    for template in templates:
                        context += f"    • {template.name}: {template.description[:60]}...\n"
                context += "\n"
        
        # Suggest entity-related actions
        if any(keyword in user_message.lower() for keyword in ['find', 'search', 'research', 'investigate']):
            context += "💡 Entity Research Suggestions:\n"
            context += "- Use our Entity Management system to organize your research targets\n"
            context += "- Create search templates for specific entity types\n"
            context += "- Track search sessions and results for better organization\n"
            context += "- Build relationship maps between entities\n\n"
        
        # Add personalized recommendations if user is provided
        if user:
            recommendations = self.get_entity_recommendations(user)
            if recommendations:
                context += recommendations
        
        return context
    
    def get_entity_recommendations(self, user, entity_type_name: str = None) -> str:
        """Get intelligent entity research recommendations for the user"""
        # Import here to avoid circular imports
        from googledorks.models import Entity, EntityType, EntitySearchTemplate, EntitySearchSession
        
        if not user or not hasattr(user, 'entity_set'):
            return ""
        
        recommendations = "\n🎯 **Intelligent Research Recommendations:**\n"
        
        # Get user's entity research activity
        user_entities = user.entity_set.all()
        recent_sessions = EntitySearchSession.objects.filter(user=user).order_by('-created_at')[:5]
        
        if not user_entities.exists():
            recommendations += "- **Get Started**: Create your first entity to begin organized research\n"
            recommendations += "- **Entity Types**: Consider researching companies, people, or organizations\n"
            recommendations += "- **Templates**: Use our pre-built search templates for quick results\n"
            return recommendations
        
        # Analyze user's research patterns
        entity_types_used = set(entity.entity_type.name for entity in user_entities)
        
        # Get unused entity types
        all_types = set(EntityType.objects.values_list('name', flat=True))
        unused_types = all_types - entity_types_used
        
        if unused_types:
            recommendations += f"- **Expand Research**: Try investigating {', '.join(list(unused_types)[:2])} entities\n"
        
        # Get popular templates not used by user
        if recent_sessions.exists():
            used_templates = set()
            for session in recent_sessions:
                if session.search_template:
                    used_templates.add(session.search_template.id)
            
            popular_templates = EntitySearchTemplate.objects.filter(
                is_active=True
            ).exclude(id__in=used_templates)[:3]
            
            if popular_templates:
                recommendations += "- **New Templates**: Try these search approaches:\n"
                for template in popular_templates:
                    recommendations += f"  • {template.name} - {template.description[:50]}...\n"
        
        # Suggest relationship mapping
        if user_entities.count() > 1:
            recommendations += "- **Relationship Mapping**: Connect your entities to discover relationships\n"
        
        # Suggest bulk operations
        if user_entities.count() > 5:
            recommendations += "- **Bulk Analysis**: Use bulk export to analyze your research data\n"
        
        return recommendations
    
    def enhance_prompt_with_context(self, user_message: str, session_id: str = None, user=None) -> str:
        """Enhance user message with relevant context"""
        enhanced_message = user_message
        
        # Add dork context if relevant
        dork_context = self.get_dork_context(user_message)
        if dork_context:
            enhanced_message += dork_context
        
        # Add entity context if relevant
        entity_context = self.get_entity_context(user_message, user)
        if entity_context:
            enhanced_message += entity_context
        
        # Add session context if available
        if session_id:
            cache_key = f"chat_context_{session_id}"
            context = cache.get(cache_key, {})
            
            if context.get('last_topic'):
                enhanced_message += f"\n\nPrevious conversation context: {context['last_topic']}"
        
        return enhanced_message
    
    def generate_response(
        self, 
        user_message: str, 
        message_history: List[Dict], 
        session_id: str = None,
        user=None
    ) -> Dict:
        """Generate a response using Gemini API"""
        
        if not self.is_configured():
            return {
                "content": "I'm sorry, but the chatbot is not properly configured. Please check the API key configuration.",
                "tokens_used": 0,
                "response_time": 0,
                "error": "API key not configured"
            }
        
        start_time = time.time()
        
        try:
            # Enhance the message with context
            enhanced_message = self.enhance_prompt_with_context(user_message, session_id, user)
            
            # Prepare conversation history
            formatted_history = self.format_message_history(message_history)
            
            # Create the full conversation content
            contents = formatted_history + [{
                "role": "user",
                "parts": [{"text": enhanced_message}]
            }]
            
            # Generate response using the new API
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt,  # Add system instruction here
                    thinking_config=types.ThinkingConfig(thinking_budget=0)  # Disable thinking for faster response
                )
            )
            
            response_time = time.time() - start_time
            
            # Estimate tokens (rough calculation)
            tokens_used = len(enhanced_message.split()) + len(response.text.split())
            
            # Cache conversation context
            if session_id:
                cache_key = f"chat_context_{session_id}"
                context = {
                    'last_topic': user_message[:100],
                    'last_response': response.text[:100]
                }
                cache.set(cache_key, context, timeout=3600)  # 1 hour
            
            return {
                "content": response.text,
                "tokens_used": tokens_used,
                "response_time": response_time,
                "metadata": {
                    "model": self.model_name,
                    "enhanced_prompt": enhanced_message != user_message
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating Gemini response: {str(e)}")
            response_time = time.time() - start_time
            
            return {
                "content": "I apologize, but I'm having trouble processing your request right now. Please try again later.",
                "tokens_used": 0,
                "response_time": response_time,
                "error": str(e)
            }
    
    def generate_chat_title(self, first_message: str) -> str:
        """Generate a title for the chat session based on the first message"""
        try:
            prompt = f"""Generate a short, descriptive title (max 50 characters) for a chat conversation that starts with this message: "{first_message}"
            
            The title should be relevant to Google dorking, security research, or the specific topic mentioned. Examples:
            - "SQL Injection Dorks"
            - "Finding Login Pages"
            - "Directory Listing Help"
            - "WordPress Vulnerabilities"
            
            Return only the title, nothing else."""
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[{
                    "role": "user",
                    "parts": [{"text": prompt}]
                }],
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(thinking_budget=0)
                )
            )
            
            title = response.text.strip().strip('"').strip("'")
            
            # Fallback if title is too long or empty
            if len(title) > 50 or len(title) < 3:
                return f"Chat about {first_message[:30]}..."
            
            return title
            
        except Exception as e:
            logger.error(f"Error generating chat title: {str(e)}")
            return f"Chat about {first_message[:30]}..."


# Global instance
gemini_service = GeminiChatService()