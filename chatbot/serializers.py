from rest_framework import serializers
from .models import ChatSession, ChatMessage, ChatFeedback, ChatMetrics
from accounts.serializers import UserSerializer


class ChatMessageSerializer(serializers.ModelSerializer):
    """Serializer for Chat Message"""
    role = serializers.SerializerMethodField()
    message = serializers.CharField(source='content')
    timestamp = serializers.DateTimeField(source='created_at', read_only=True)
    
    class Meta:
        model = ChatMessage
        fields = [
            'id', 'session', 'role', 'message', 'timestamp',
            'tokens_used', 'response_time', 'metadata'
        ]
        read_only_fields = ['id', 'timestamp']
    
    def get_role(self, obj):
        """Map message_type to role for frontend"""
        if obj.message_type == 'bot':
            return 'assistant'
        return obj.message_type  # 'user' or 'system'


class ChatSessionSerializer(serializers.ModelSerializer):
    """Serializer for Chat Session"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    entity_name = serializers.CharField(source='entity.name', read_only=True)
    message_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatSession
        fields = [
            'id', 'user', 'user_username', 'entity', 'entity_name',
            'title', 'is_active', 'created_at', 'updated_at',
            'message_count', 'last_message'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_message_count(self, obj):
        return obj.messages.count()
    
    def get_last_message(self, obj):
        last_message = obj.messages.order_by('-created_at').first()
        if last_message:
            return {
                'content': last_message.content[:100],
                'created_at': last_message.created_at
            }
        return None
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)


class ChatSessionDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Chat Session with messages"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    entity_name = serializers.CharField(source='entity.name', read_only=True)
    messages = ChatMessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatSession
        fields = [
            'id', 'user', 'user_username', 'entity', 'entity_name',
            'title', 'is_active', 'created_at', 'updated_at',
            'messages', 'message_count'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_message_count(self, obj):
        return obj.messages.count()


class ChatFeedbackSerializer(serializers.ModelSerializer):
    """Serializer for Chat Feedback"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    message_content = serializers.CharField(source='message.content', read_only=True)
    
    class Meta:
        model = ChatFeedback
        fields = [
            'id', 'message', 'message_content', 'user', 'user_username',
            'feedback_type', 'comment', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)


class SendMessageSerializer(serializers.Serializer):
    """Serializer for sending a new message"""
    session_id = serializers.UUIDField(required=False, allow_null=True)
    message = serializers.CharField(required=True)
    title = serializers.CharField(required=False, allow_blank=True)
    
    def validate_message(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message cannot be empty")
        return value.strip()


class ChatMetricsSerializer(serializers.ModelSerializer):
    """Serializer for Chat Metrics"""
    
    class Meta:
        model = ChatMetrics
        fields = [
            'id', 'date', 'total_sessions', 'total_messages',
            'avg_response_time', 'avg_tokens_per_message',
            'positive_feedback_count', 'negative_feedback_count'
        ]
        read_only_fields = ['id']
