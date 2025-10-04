from rest_framework import viewsets, status, filters, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Count, Avg
from django.utils import timezone
import uuid
import logging

logger = logging.getLogger(__name__)

from .models import ChatSession, ChatMessage, ChatFeedback, ChatMetrics
from .serializers import (
    ChatSessionSerializer, ChatSessionDetailSerializer,
    ChatMessageSerializer, ChatFeedbackSerializer,
    SendMessageSerializer, ChatMetricsSerializer
)
from .services import GeminiChatService


class ChatSessionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing chat sessions
    
    list: Get all user's chat sessions
    retrieve: Get a specific session with messages
    create: Create a new chat session
    update: Update a session (title only)
    destroy: Delete (deactivate) a session
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-updated_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ChatSessionDetailSerializer
        return ChatSessionSerializer
    
    def get_queryset(self):
        # Users can only see their own sessions
        return ChatSession.objects.filter(
            user=self.request.user,
            is_active=True
        ).prefetch_related('messages')
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete - mark as inactive"""
        session = self.get_object()
        session.is_active = False
        session.save()
        return Response({'message': 'Session deleted successfully'})
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """Get all messages for this session"""
        session = self.get_object()
        messages = session.messages.order_by('created_at')
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent chat sessions"""
        limit = int(request.query_params.get('limit', 10))
        sessions = self.get_queryset()[:limit]
        serializer = self.get_serializer(sessions, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def start_session(self, request):
        """Start a new chat session"""
        title = request.data.get('title', 'New Chat')
        entity_id = request.data.get('entity_id')
        
        session = ChatSession.objects.create(
            user=request.user,
            title=title[:200]
        )
        
        # If entity_id is provided, associate it
        if entity_id:
            try:
                from googledorks.models import Entity
                entity = Entity.objects.get(id=entity_id, user=request.user)
                session.entity = entity
                session.save()
            except:
                pass
        
        serializer = self.get_serializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """Send a message to the chatbot and get AI response"""
        session = self.get_object()
        message_content = request.data.get('message', '').strip()
        
        if not message_content:
            return Response(
                {'error': 'Message content is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Save user message
        user_message = ChatMessage.objects.create(
            session=session,
            message_type='user',
            content=message_content
        )
        
        # Get message history
        previous_messages = ChatMessage.objects.filter(
            session=session
        ).order_by('-created_at')[:10]
        
        message_history = []
        for msg in reversed(list(previous_messages)):
            message_history.append({
                'message_type': msg.message_type,
                'content': msg.content
            })
        
        # Get user-specific Gemini service
        gemini_service = GeminiChatService.get_service_for_user(request.user)
        
        # Generate AI response
        if gemini_service.is_configured():
            try:
                response_data = gemini_service.generate_response(
                    message_content,
                    message_history,
                    str(session.id),
                    request.user
                )
            except Exception as e:
                logger.error(f"Error generating Gemini response: {str(e)}")
                # Create fallback response
                bot_message = ChatMessage.objects.create(
                    session=session,
                    message_type='bot',
                    content=f"I apologize, but I encountered an error processing your request. Please try again.",
                    tokens_used=0,
                    response_time=0
                )
                session.updated_at = timezone.now()
                session.save()
                return Response(ChatMessageSerializer(bot_message).data)
            
            # Save bot response
            bot_message = ChatMessage.objects.create(
                session=session,
                message_type='bot',
                content=response_data['content'],
                tokens_used=response_data.get('tokens_used', 0),
                response_time=response_data.get('response_time', 0),
                metadata=response_data.get('metadata', {})
            )
            
            # Update session title if this is the first exchange
            if session.messages.count() <= 2:  # User + Bot message
                session.title = gemini_service.generate_chat_title(message_content)
                session.save()
        else:
            # Fallback response when API is not configured
            bot_message = ChatMessage.objects.create(
                session=session,
                message_type='bot',
                content="I'm sorry, but the AI assistant is not properly configured. Please set up your Gemini API key to use this feature.",
                tokens_used=0,
                response_time=0
            )
        
        # Update session timestamp
        session.updated_at = timezone.now()
        session.save()
        
        # Return the bot message
        return Response(ChatMessageSerializer(bot_message).data)
    
    @action(detail=False, methods=['get'])
    def check_configuration(self, request):
        """Check if chatbot is properly configured"""
        gemini_service = GeminiChatService.get_service_for_user(request.user)
        
        is_configured = gemini_service.is_configured()
        
        return Response({
            'configured': is_configured,
            'message': 'Chatbot is ready!' if is_configured else 'Gemini API key not configured. Please add GEMINI_API_KEY to your Django settings.'
        })
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get user's chatbot statistics"""
        user_sessions = self.get_queryset()
        total_sessions = user_sessions.count()
        total_messages = ChatMessage.objects.filter(
            session__in=user_sessions
        ).count()
        
        avg_messages = total_messages / total_sessions if total_sessions > 0 else 0
        
        return Response({
            'total_sessions': total_sessions,
            'total_messages': total_messages,
            'avg_messages_per_session': round(avg_messages, 1)
        })


class ChatMessageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing chat messages
    
    list: Get all messages from user's sessions
    retrieve: Get a specific message
    """
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['created_at']
    
    def get_queryset(self):
        # Users can only see messages from their own sessions
        return ChatMessage.objects.filter(
            session__user=self.request.user,
            session__is_active=True
        ).select_related('session')


class ChatFeedbackViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing chat feedback
    
    list: Get all user's feedback
    retrieve: Get specific feedback
    create: Submit new feedback
    update: Update existing feedback
    destroy: Delete feedback
    """
    serializer_class = ChatFeedbackSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        # Users can only see their own feedback
        return ChatFeedback.objects.filter(
            user=self.request.user
        ).select_related('message', 'user')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    """
    Send a message to the chatbot and get AI response
    
    POST /api/chatbot/send-message/
    Body: {
        "session_id": "uuid" (optional),
        "message": "your message",
        "title": "session title" (optional, for new sessions)
    }
    """
    serializer = SendMessageSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    session_id = serializer.validated_data.get('session_id')
    message_content = serializer.validated_data['message']
    title = serializer.validated_data.get('title', 'New Chat')
    
    # Get or create session
    if session_id:
        try:
            session = ChatSession.objects.get(id=session_id, user=request.user)
        except ChatSession.DoesNotExist:
            return Response(
                {'error': 'Session not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    else:
        session = ChatSession.objects.create(
            user=request.user,
            title=title[:200]
        )
    
    # Save user message
    user_message = ChatMessage.objects.create(
        session=session,
        message_type='user',
        content=message_content
    )
    
    # Get message history
    previous_messages = ChatMessage.objects.filter(
        session=session
    ).order_by('-created_at')[:10]
    
    message_history = []
    for msg in reversed(list(previous_messages)):
        message_history.append({
            'message_type': msg.message_type,
            'content': msg.content
        })
    
    # Get user-specific Gemini service
    gemini_service = GeminiChatService.get_service_for_user(request.user)
    
    # Generate AI response
    if gemini_service.is_configured():
        try:
            response_data = gemini_service.generate_response(
                message_content,
                message_history,
                str(session.id),
                request.user
            )
        except Exception as e:
            logger.error(f"Error generating Gemini response: {str(e)}")
            # Create fallback response
            bot_message = ChatMessage.objects.create(
                session=session,
                message_type='bot',
                content=f"I apologize, but I encountered an error processing your request. Please try again.",
                tokens_used=0,
                response_time=0
            )
            
            return Response({
                'success': False,
                'session_id': str(session.id),
                'session_title': session.title,
                'user_message': ChatMessageSerializer(user_message).data,
                'bot_response': ChatMessageSerializer(bot_message).data,
                'error': 'Failed to generate AI response'
            })
        
        # Save bot response
        bot_message = ChatMessage.objects.create(
            session=session,
            message_type='bot',
            content=response_data['content'],
            tokens_used=response_data.get('tokens_used', 0),
            response_time=response_data.get('response_time', 0),
            metadata=response_data.get('metadata', {})
        )
        
        # Update session title if this is the first exchange
        if session.messages.count() <= 2:  # User + Bot message
            session.title = gemini_service.generate_chat_title(message_content)
            session.save()
        
        # Update session timestamp
        session.updated_at = timezone.now()
        session.save()
        
        return Response({
            'success': True,
            'session_id': str(session.id),
            'session_title': session.title,
            'user_message': ChatMessageSerializer(user_message).data,
            'bot_response': ChatMessageSerializer(bot_message).data,
        })
    else:
        # Fallback response when API is not configured
        bot_message = ChatMessage.objects.create(
            session=session,
            message_type='bot',
            content="I'm sorry, but the AI assistant is not properly configured. Please set up your Gemini API key to use this feature.",
            tokens_used=0,
            response_time=0
        )
        
        return Response({
            'success': True,
            'session_id': str(session.id),
            'session_title': session.title,
            'user_message': ChatMessageSerializer(user_message).data,
            'bot_response': ChatMessageSerializer(bot_message).data,
            'warning': 'AI not configured. Please setup API key.'
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_session(request):
    """
    Start a new chat session
    
    POST /api/chatbot/start-session/
    Body: {
        "title": "Session title" (optional)
    }
    """
    title = request.data.get('title', 'New Chat')
    
    session = ChatSession.objects.create(
        user=request.user,
        title=title[:200]
    )
    
    return Response({
        'success': True,
        'session': ChatSessionSerializer(session, context={'request': request}).data
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def statistics(request):
    """
    Get chatbot usage statistics (admin only)
    
    GET /api/chatbot/statistics/
    """
    from datetime import timedelta
    
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    metrics = ChatMetrics.objects.filter(
        date__range=[start_date, end_date]
    ).order_by('-date')
    
    # Overall stats
    total_sessions = ChatSession.objects.count()
    total_messages = ChatMessage.objects.count()
    active_users = ChatSession.objects.values('user').distinct().count()
    
    avg_response_time = ChatMessage.objects.filter(
        message_type='bot',
        response_time__isnull=False
    ).aggregate(avg_time=Avg('response_time'))['avg_time'] or 0
    
    avg_tokens = ChatMessage.objects.filter(
        tokens_used__gt=0
    ).aggregate(avg_tokens=Avg('tokens_used'))['avg_tokens'] or 0
    
    # Feedback stats
    positive_feedback = ChatFeedback.objects.filter(
        feedback_type='positive'
    ).count()
    
    negative_feedback = ChatFeedback.objects.filter(
        feedback_type='negative'
    ).count()
    
    return Response({
        'total_sessions': total_sessions,
        'total_messages': total_messages,
        'active_users': active_users,
        'avg_response_time': round(avg_response_time, 2),
        'avg_tokens_per_message': round(avg_tokens, 0),
        'positive_feedback': positive_feedback,
        'negative_feedback': negative_feedback,
        'metrics': ChatMetricsSerializer(metrics, many=True).data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_configuration(request):
    """
    Check if chatbot is properly configured for the user
    
    GET /api/chatbot/check-configuration/
    """
    gemini_service = GeminiChatService.get_service_for_user(request.user)
    
    return Response({
        'is_configured': gemini_service.is_configured(),
        'has_api_key': request.user.has_gemini_api_key() if hasattr(request.user, 'has_gemini_api_key') else False,
        'model': gemini_service.model_name if gemini_service.is_configured() else None
    })
