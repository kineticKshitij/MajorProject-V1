from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Avg
from django.utils import timezone
import json
import asyncio
import uuid
from datetime import datetime, timedelta

from .models import ChatSession, ChatMessage, ChatFeedback, ChatMetrics
from .services import GeminiChatService


def chatbot_home(request):
    """Main chatbot interface"""
    # Get recent sessions for the user or anonymous sessions
    recent_sessions = []
    gemini_service = None
    
    if request.user.is_authenticated:
        recent_sessions = ChatSession.objects.filter(
            user=request.user,
            is_active=True
        ).order_by('-updated_at')[:10]
        gemini_service = GeminiChatService.get_service_for_user(request.user)
    else:
        gemini_service = GeminiChatService()
    
    context = {
        'recent_sessions': recent_sessions,
        'is_configured': gemini_service.is_configured(),
        'has_api_key': request.user.is_authenticated and hasattr(request.user, 'has_gemini_api_key') and request.user.has_gemini_api_key(),
    }
    return render(request, 'chatbot/chat_interface.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def start_new_session(request):
    """Start a new chat session"""
    try:
        data = json.loads(request.body)
        title = data.get('title', 'New Chat')
        
        session = ChatSession.objects.create(
            user=request.user if request.user.is_authenticated else None,
            title=title[:200]  # Limit title length
        )
        
        return JsonResponse({
            'success': True,
            'session_id': str(session.id),
            'title': session.title
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def send_message(request):
    """Send a message and get AI response"""
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        message_content = data.get('message', '').strip()
        
        if not message_content:
            return JsonResponse({
                'success': False,
                'error': 'Message content is required'
            }, status=400)
        
        if not session_id:
            return JsonResponse({
                'success': False,
                'error': 'Session ID is required'
            }, status=400)
        
        # Get or create session
        try:
            session = ChatSession.objects.get(id=session_id)
        except ChatSession.DoesNotExist:
            session = ChatSession.objects.create(
                user=request.user if request.user.is_authenticated else None,
                title='New Chat'
            )
        
        # Save user message
        user_message = ChatMessage.objects.create(
            session=session,
            message_type='user',
            content=message_content
        )
        
        # Get message history for context
        previous_messages = ChatMessage.objects.filter(
            session=session
        ).order_by('-created_at')[:10]
        
        message_history = []
        for msg in reversed(previous_messages):
            message_history.append({
                'message_type': msg.message_type,
                'content': msg.content
            })
        
        # Get user-specific Gemini service
        if request.user.is_authenticated:
            gemini_service = GeminiChatService.get_service_for_user(request.user)
        else:
            gemini_service = GeminiChatService()
        
        # Generate AI response
        if gemini_service.is_configured():
            # Use asyncio to handle async function
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                response_data = loop.run_until_complete(
                    gemini_service.generate_response(
                        message_content,
                        message_history,
                        str(session.id)
                    )
                )
            finally:
                loop.close()
            
            # Save bot response
            bot_message = ChatMessage.objects.create(
                session=session,
                message_type='bot',
                content=response_data['content'],
                tokens_used=response_data.get('tokens_used', 0),
                response_time=response_data.get('response_time', 0),
                metadata=response_data.get('metadata', {})
            )
            
            # Update session title if this is the first message
            if session.get_messages_count() <= 2:  # User + Bot message
                session.title = gemini_service.generate_chat_title(message_content)
                session.save()
            
            # Update session timestamp
            session.updated_at = timezone.now()
            session.save()
            
        else:
            # Fallback response when API is not configured
            api_key_setup_url = ""
            if request.user.is_authenticated:
                api_key_setup_url = f"<br><a href='/accounts/api-key-setup/' class='btn btn-primary btn-sm mt-2'>Setup API Key</a>"
            
            bot_message = ChatMessage.objects.create(
                session=session,
                message_type='bot',
                content=f"I'm sorry, but I'm not properly configured right now. Please set up your Gemini API key to use the AI assistant.{api_key_setup_url}",
                tokens_used=0,
                response_time=0
            )
        
        return JsonResponse({
            'success': True,
            'user_message': {
                'id': str(user_message.id),
                'content': user_message.content,
                'created_at': user_message.created_at.isoformat()
            },
            'bot_response': {
                'id': str(bot_message.id),
                'content': bot_message.content,
                'created_at': bot_message.created_at.isoformat(),
                'tokens_used': bot_message.tokens_used,
                'response_time': bot_message.response_time
            },
            'session_title': session.title
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def get_session_messages(request, session_id):
    """Get all messages for a session"""
    try:
        session = get_object_or_404(ChatSession, id=session_id)
        
        # Check permission (user owns session or is admin)
        if (session.user and session.user != request.user and 
            not request.user.is_staff):
            return JsonResponse({
                'success': False,
                'error': 'Permission denied'
            }, status=403)
        
        messages = ChatMessage.objects.filter(session=session).order_by('created_at')
        
        messages_data = []
        for msg in messages:
            messages_data.append({
                'id': str(msg.id),
                'type': msg.message_type,
                'content': msg.content,
                'created_at': msg.created_at.isoformat(),
                'tokens_used': msg.tokens_used,
                'response_time': msg.response_time
            })
        
        return JsonResponse({
            'success': True,
            'session': {
                'id': str(session.id),
                'title': session.title,
                'created_at': session.created_at.isoformat()
            },
            'messages': messages_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def submit_feedback(request):
    """Submit feedback for a bot response"""
    try:
        data = json.loads(request.body)
        message_id = data.get('message_id')
        feedback_type = data.get('feedback_type')
        comment = data.get('comment', '')
        
        if not message_id or not feedback_type:
            return JsonResponse({
                'success': False,
                'error': 'Message ID and feedback type are required'
            }, status=400)
        
        message = get_object_or_404(ChatMessage, id=message_id)
        
        # Create or update feedback
        feedback, created = ChatFeedback.objects.update_or_create(
            message=message,
            user=request.user if request.user.is_authenticated else None,
            defaults={
                'feedback_type': feedback_type,
                'comment': comment
            }
        )
        
        return JsonResponse({
            'success': True,
            'created': created
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
def user_sessions(request):
    """List user's chat sessions"""
    sessions = ChatSession.objects.filter(
        user=request.user,
        is_active=True
    ).annotate(
        message_count=Count('messages')
    ).order_by('-updated_at')
    
    paginator = Paginator(sessions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'sessions': page_obj,
        'total_sessions': sessions.count()
    }
    
    return render(request, 'chatbot/user_sessions.html', context)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_session(request, session_id):
    """Delete a chat session"""
    try:
        session = get_object_or_404(ChatSession, id=session_id)
        
        # Check permission
        if (session.user and session.user != request.user and 
            not request.user.is_staff):
            return JsonResponse({
                'success': False,
                'error': 'Permission denied'
            }, status=403)
        
        session.is_active = False
        session.save()
        
        return JsonResponse({'success': True})
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def chatbot_stats(request):
    """Display chatbot usage statistics"""
    if not request.user.is_staff:
        return JsonResponse({
            'success': False,
            'error': 'Permission denied'
        }, status=403)
    
    # Get recent metrics
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    metrics = ChatMetrics.objects.filter(
        date__range=[start_date, end_date]
    ).order_by('-date')
    
    # Get overall stats
    total_sessions = ChatSession.objects.count()
    total_messages = ChatMessage.objects.count()
    avg_response_time = ChatMessage.objects.filter(
        message_type='bot',
        response_time__isnull=False
    ).aggregate(avg_time=Avg('response_time'))['avg_time'] or 0
    
    # Get service configuration status
    if request.user.is_authenticated:
        gemini_service = GeminiChatService.get_service_for_user(request.user)
    else:
        gemini_service = GeminiChatService()
    
    context = {
        'metrics': metrics,
        'total_sessions': total_sessions,
        'total_messages': total_messages,
        'avg_response_time': round(avg_response_time, 2),
        'is_configured': gemini_service.is_configured()
    }
    
    return render(request, 'chatbot/stats.html', context)
