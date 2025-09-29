from django.contrib import admin
from django.utils.html import format_html
from .models import ChatSession, ChatMessage, ChatFeedback, ChatMetrics


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'get_messages_count', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['title', 'user__username']
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    def get_messages_count(self, obj):
        return obj.get_messages_count()
    get_messages_count.short_description = 'Messages'


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'message_type', 'content_preview', 'tokens_used', 'response_time', 'created_at']
    list_filter = ['message_type', 'created_at']
    search_fields = ['content', 'session__title']
    readonly_fields = ['id', 'created_at']
    date_hierarchy = 'created_at'
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'


@admin.register(ChatFeedback)
class ChatFeedbackAdmin(admin.ModelAdmin):
    list_display = ['message', 'user', 'feedback_type', 'created_at']
    list_filter = ['feedback_type', 'created_at']
    search_fields = ['comment', 'user__username']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(ChatMetrics)
class ChatMetricsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_sessions', 'total_messages', 'total_tokens_used', 'average_response_time', 'unique_users']
    list_filter = ['date']
    readonly_fields = ['date']
    date_hierarchy = 'date'
    
    def has_add_permission(self, request):
        # Metrics are auto-generated, don't allow manual creation
        return False
