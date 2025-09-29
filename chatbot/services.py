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
        
        # Add system prompt first
        formatted_messages.append({
            "role": "system",
            "parts": [{"text": self.system_prompt}]
        })
        
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
    
    def enhance_prompt_with_context(self, user_message: str, session_id: str = None) -> str:
        """Enhance user message with relevant context"""
        enhanced_message = user_message
        
        # Add dork context if relevant
        dork_context = self.get_dork_context(user_message)
        if dork_context:
            enhanced_message += dork_context
        
        # Add session context if available
        if session_id:
            cache_key = f"chat_context_{session_id}"
            context = cache.get(cache_key, {})
            
            if context.get('last_topic'):
                enhanced_message += f"\n\nPrevious conversation context: {context['last_topic']}"
        
        return enhanced_message
    
    async def generate_response(
        self, 
        user_message: str, 
        message_history: List[Dict], 
        session_id: str = None
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
            enhanced_message = self.enhance_prompt_with_context(user_message, session_id)
            
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