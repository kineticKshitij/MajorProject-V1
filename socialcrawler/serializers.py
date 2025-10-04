from rest_framework import serializers
from .models import (
    CrawlJob, SocialProfile, SocialPost, 
    SocialMetrics, CrawlSchedule
)


class SocialPostSerializer(serializers.ModelSerializer):
    """Serializer for social media posts"""
    profile_username = serializers.CharField(source='profile.username', read_only=True)
    platform = serializers.CharField(source='profile.platform', read_only=True)
    
    class Meta:
        model = SocialPost
        fields = [
            'id', 'profile', 'profile_username', 'platform', 'crawl_job',
            'post_id', 'post_url', 'content', 'media_urls', 'media_type',
            'likes_count', 'comments_count', 'shares_count', 'views_count',
            'posted_at', 'language', 'hashtags', 'mentions',
            'sentiment', 'topics', 'crawled_at', 'raw_data'
        ]
        read_only_fields = ['id', 'crawled_at']


class SocialProfileSerializer(serializers.ModelSerializer):
    """Serializer for social media profiles"""
    posts = SocialPostSerializer(many=True, read_only=True)
    post_count = serializers.IntegerField(source='posts.count', read_only=True)
    entity_name = serializers.CharField(source='entity.name', read_only=True, allow_null=True)
    
    class Meta:
        model = SocialProfile
        fields = [
            'id', 'crawl_job', 'entity', 'entity_name',
            'platform', 'username', 'user_id', 'profile_url',
            'display_name', 'bio', 'avatar_url', 'banner_url',
            'followers_count', 'following_count', 'posts_count', 'verified',
            'location', 'website', 'joined_date',
            'crawled_at', 'last_updated', 'raw_data',
            'posts', 'post_count'
        ]
        read_only_fields = ['id', 'crawled_at', 'last_updated']


class SocialProfileListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for profile lists"""
    entity_name = serializers.CharField(source='entity.name', read_only=True, allow_null=True)
    post_count = serializers.IntegerField(source='posts.count', read_only=True)
    
    class Meta:
        model = SocialProfile
        fields = [
            'id', 'platform', 'username', 'user_id', 'profile_url',
            'display_name', 'avatar_url', 'followers_count',
            'following_count', 'posts_count', 'verified',
            'entity', 'entity_name', 'post_count', 'crawled_at'
        ]
        read_only_fields = ['id', 'crawled_at']


class CrawlJobSerializer(serializers.ModelSerializer):
    """Serializer for crawl jobs"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    entity_name = serializers.CharField(source='entity.name', read_only=True, allow_null=True)
    duration_seconds = serializers.FloatField(source='duration', read_only=True)
    profiles = SocialProfileListSerializer(many=True, read_only=True)
    
    class Meta:
        model = CrawlJob
        fields = [
            'id', 'user', 'user_username', 'entity', 'entity_name',
            'platform', 'target_username', 'target_url',
            'crawl_posts', 'crawl_followers', 'crawl_following',
            'max_posts', 'max_followers',
            'status', 'progress', 'profiles_found', 'posts_found',
            'error_message', 'created_at', 'started_at', 'completed_at',
            'duration_seconds', 'metadata', 'profiles'
        ]
        read_only_fields = [
            'id', 'user', 'status', 'progress', 'profiles_found',
            'posts_found', 'error_message', 'created_at', 'started_at',
            'completed_at'
        ]


class CrawlJobListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for job lists"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    entity_name = serializers.CharField(source='entity.name', read_only=True, allow_null=True)
    duration_seconds = serializers.FloatField(source='duration', read_only=True)
    
    class Meta:
        model = CrawlJob
        fields = [
            'id', 'user_username', 'entity', 'entity_name',
            'platform', 'target_username', 'status', 'progress',
            'profiles_found', 'posts_found', 'created_at',
            'completed_at', 'duration_seconds'
        ]
        read_only_fields = ['id', 'created_at', 'completed_at']


class CreateCrawlJobSerializer(serializers.ModelSerializer):
    """Serializer for creating crawl jobs"""
    
    class Meta:
        model = CrawlJob
        fields = [
            'entity', 'platform', 'target_username', 'target_url',
            'crawl_posts', 'crawl_followers', 'crawl_following',
            'max_posts', 'max_followers'
        ]
    
    def validate(self, data):
        """Validate that at least username or URL is provided"""
        target_username = data.get('target_username', '').strip()
        target_url = data.get('target_url', '').strip()
        
        if not target_username and not target_url:
            raise serializers.ValidationError({
                'target_username': "Either target_username or target_url must be provided"
            })
        
        # If URL is provided but no username, try to extract username from URL
        if target_url and not target_username:
            # Extract username from common URL patterns
            # e.g., https://github.com/username -> username
            import re
            username_match = re.search(r'/([^/]+?)/?$', target_url.rstrip('/'))
            if username_match:
                data['target_username'] = username_match.group(1)
        
        return data
    
    def validate_target_username(self, value):
        """Validate username format"""
        if not value or not value.strip():
            return ''
        # Remove @ symbol if present
        return value.lstrip('@').strip()
    
    def validate_max_posts(self, value):
        """Validate max posts limit"""
        if value is not None:
            if value < 1:
                raise serializers.ValidationError("Must crawl at least 1 post")
            if value > 1000:
                raise serializers.ValidationError("Cannot crawl more than 1000 posts at once")
        return value
    
    def validate_max_followers(self, value):
        """Validate max followers limit"""
        if value is not None:
            if value < 0:
                raise serializers.ValidationError("Cannot be negative")
            if value > 10000:
                raise serializers.ValidationError("Cannot crawl more than 10000 followers at once")
        return value


class SocialMetricsSerializer(serializers.ModelSerializer):
    """Serializer for social metrics"""
    profile_username = serializers.CharField(source='profile.username', read_only=True)
    platform = serializers.CharField(source='profile.platform', read_only=True)
    
    class Meta:
        model = SocialMetrics
        fields = [
            'id', 'profile', 'profile_username', 'platform', 'date',
            'followers_count', 'following_count', 'posts_count',
            'avg_likes', 'avg_comments', 'avg_shares', 'engagement_rate',
            'posts_today', 'recorded_at'
        ]
        read_only_fields = ['id', 'recorded_at']


class CrawlScheduleSerializer(serializers.ModelSerializer):
    """Serializer for crawl schedules"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    entity_name = serializers.CharField(source='entity.name', read_only=True, allow_null=True)
    
    class Meta:
        model = CrawlSchedule
        fields = [
            'id', 'user', 'user_username', 'entity', 'entity_name',
            'name', 'platform', 'target_username', 'frequency',
            'is_active', 'last_run', 'next_run', 'crawl_config',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'last_run', 'created_at', 'updated_at']


class PostAnalyticsSerializer(serializers.Serializer):
    """Serializer for post analytics"""
    total_posts = serializers.IntegerField()
    total_likes = serializers.IntegerField()
    total_comments = serializers.IntegerField()
    total_shares = serializers.IntegerField()
    avg_likes = serializers.FloatField()
    avg_comments = serializers.FloatField()
    avg_shares = serializers.FloatField()
    engagement_rate = serializers.FloatField()
    top_hashtags = serializers.ListField(child=serializers.DictField())
    post_frequency = serializers.DictField()


class ProfileAnalyticsSerializer(serializers.Serializer):
    """Serializer for profile analytics"""
    total_profiles = serializers.IntegerField()
    total_followers = serializers.IntegerField()
    total_posts = serializers.IntegerField()
    avg_followers = serializers.FloatField()
    verified_count = serializers.IntegerField()
    platform_distribution = serializers.DictField()
    top_profiles = serializers.ListField(child=serializers.DictField())
