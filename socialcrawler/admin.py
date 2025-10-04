from django.contrib import admin
from .models import (
    CrawlJob, SocialProfile, SocialPost,
    SocialMetrics, CrawlSchedule
)


@admin.register(CrawlJob)
class CrawlJobAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'platform', 'target_username', 'status', 'progress', 'created_at']
    list_filter = ['status', 'platform', 'created_at']
    search_fields = ['target_username', 'user__username']
    readonly_fields = ['id', 'created_at', 'started_at', 'completed_at']
    list_per_page = 50
    
    fieldsets = (
        ('Job Info', {
            'fields': ('id', 'user', 'entity', 'platform', 'target_username', 'target_url')
        }),
        ('Configuration', {
            'fields': ('crawl_posts', 'crawl_followers', 'crawl_following', 'max_posts', 'max_followers')
        }),
        ('Status', {
            'fields': ('status', 'progress', 'profiles_found', 'posts_found', 'error_message')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'started_at', 'completed_at')
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
    )


@admin.register(SocialProfile)
class SocialProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'platform', 'followers_count', 'posts_count', 'verified', 'crawled_at']
    list_filter = ['platform', 'verified', 'crawled_at']
    search_fields = ['username', 'display_name', 'bio']
    readonly_fields = ['id', 'crawled_at', 'last_updated']
    list_per_page = 50
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('id', 'crawl_job', 'entity', 'platform', 'username', 'user_id', 'profile_url')
        }),
        ('Profile Data', {
            'fields': ('display_name', 'bio', 'avatar_url', 'banner_url')
        }),
        ('Metrics', {
            'fields': ('followers_count', 'following_count', 'posts_count', 'verified')
        }),
        ('Additional Info', {
            'fields': ('location', 'website', 'joined_date')
        }),
        ('Timestamps', {
            'fields': ('crawled_at', 'last_updated')
        }),
        ('Raw Data', {
            'fields': ('raw_data',),
            'classes': ('collapse',)
        }),
    )


@admin.register(SocialPost)
class SocialPostAdmin(admin.ModelAdmin):
    list_display = ['post_id', 'profile', 'likes_count', 'comments_count', 'posted_at']
    list_filter = ['profile__platform', 'posted_at', 'media_type', 'sentiment']
    search_fields = ['content', 'post_id']
    readonly_fields = ['id', 'crawled_at']
    list_per_page = 50
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('id', 'profile', 'crawl_job', 'post_id', 'post_url')
        }),
        ('Content', {
            'fields': ('content', 'media_urls', 'media_type')
        }),
        ('Engagement', {
            'fields': ('likes_count', 'comments_count', 'shares_count', 'views_count')
        }),
        ('Metadata', {
            'fields': ('posted_at', 'language', 'hashtags', 'mentions')
        }),
        ('Analysis', {
            'fields': ('sentiment', 'topics')
        }),
        ('Timestamps', {
            'fields': ('crawled_at',)
        }),
        ('Raw Data', {
            'fields': ('raw_data',),
            'classes': ('collapse',)
        }),
    )


@admin.register(SocialMetrics)
class SocialMetricsAdmin(admin.ModelAdmin):
    list_display = ['profile', 'date', 'followers_count', 'engagement_rate', 'posts_today']
    list_filter = ['date', 'profile__platform']
    search_fields = ['profile__username']
    readonly_fields = ['id', 'recorded_at']
    list_per_page = 50


@admin.register(CrawlSchedule)
class CrawlScheduleAdmin(admin.ModelAdmin):
    list_display = ['name', 'platform', 'target_username', 'frequency', 'is_active', 'next_run']
    list_filter = ['platform', 'frequency', 'is_active']
    search_fields = ['name', 'target_username']
    readonly_fields = ['id', 'last_run', 'created_at', 'updated_at']
    list_per_page = 50
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('id', 'user', 'entity', 'name', 'platform', 'target_username')
        }),
        ('Schedule', {
            'fields': ('frequency', 'is_active', 'last_run', 'next_run')
        }),
        ('Configuration', {
            'fields': ('crawl_config',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
