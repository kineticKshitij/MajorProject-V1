from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from googledorks.models import Entity
import uuid

User = get_user_model()


class SocialPlatform(models.TextChoices):
    """Social media platforms"""
    TWITTER = 'twitter', 'Twitter/X'
    LINKEDIN = 'linkedin', 'LinkedIn'
    INSTAGRAM = 'instagram', 'Instagram'
    FACEBOOK = 'facebook', 'Facebook'
    GITHUB = 'github', 'GitHub'
    REDDIT = 'reddit', 'Reddit'
    TIKTOK = 'tiktok', 'TikTok'
    YOUTUBE = 'youtube', 'YouTube'


class CrawlStatus(models.TextChoices):
    """Status of crawl jobs"""
    PENDING = 'pending', 'Pending'
    IN_PROGRESS = 'in_progress', 'In Progress'
    COMPLETED = 'completed', 'Completed'
    FAILED = 'failed', 'Failed'
    CANCELLED = 'cancelled', 'Cancelled'


class CrawlJob(models.Model):
    """Represents a social media crawling job"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crawl_jobs')
    entity = models.ForeignKey(Entity, on_delete=models.SET_NULL, null=True, blank=True, related_name='crawl_jobs')
    
    # Job details
    platform = models.CharField(max_length=20, choices=SocialPlatform.choices)
    target_username = models.CharField(max_length=255, blank=True, help_text="Username or handle to crawl")
    target_url = models.URLField(blank=True, help_text="Direct URL to profile")
    
    # Crawl configuration
    crawl_posts = models.BooleanField(default=True, help_text="Crawl user's posts")
    crawl_followers = models.BooleanField(default=False, help_text="Crawl followers list")
    crawl_following = models.BooleanField(default=False, help_text="Crawl following list")
    max_posts = models.IntegerField(default=100, help_text="Maximum posts to crawl")
    max_followers = models.IntegerField(default=1000, help_text="Maximum followers to crawl")
    
    # Status
    status = models.CharField(max_length=20, choices=CrawlStatus.choices, default=CrawlStatus.PENDING)
    progress = models.IntegerField(default=0, help_text="Progress percentage (0-100)")
    
    # Results
    profiles_found = models.IntegerField(default=0)
    posts_found = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['platform', 'status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.platform} - {self.target_username} ({self.status})"
    
    @property
    def duration(self):
        """Calculate job duration"""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        elif self.started_at:
            return (timezone.now() - self.started_at).total_seconds()
        return 0


class SocialProfile(models.Model):
    """Represents a social media profile"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    crawl_job = models.ForeignKey(CrawlJob, on_delete=models.CASCADE, related_name='profiles')
    entity = models.ForeignKey(Entity, on_delete=models.SET_NULL, null=True, blank=True, related_name='social_profiles')
    
    # Platform info
    platform = models.CharField(max_length=20, choices=SocialPlatform.choices)
    username = models.CharField(max_length=255, db_index=True)
    user_id = models.CharField(max_length=255, blank=True, default='', help_text="Platform-specific user ID")
    profile_url = models.URLField()
    
    # Profile data
    display_name = models.CharField(max_length=255, blank=True, default='')
    bio = models.TextField(blank=True, default='')
    avatar_url = models.URLField(blank=True, default='')
    banner_url = models.URLField(blank=True, default='')
    
    # Metrics
    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    posts_count = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)
    
    # Additional info
    location = models.CharField(max_length=255, blank=True, default='')
    website = models.URLField(blank=True, default='')
    joined_date = models.DateField(null=True, blank=True)
    
    # Timestamps
    crawled_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    # Raw data
    raw_data = models.JSONField(default=dict, blank=True, help_text="Complete raw profile data")
    
    class Meta:
        ordering = ['-crawled_at']
        unique_together = [['platform', 'username', 'crawl_job']]
        indexes = [
            models.Index(fields=['platform', 'username']),
            models.Index(fields=['crawled_at']),
        ]
    
    def __str__(self):
        return f"{self.platform} - @{self.username}"


class SocialPost(models.Model):
    """Represents a social media post"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(SocialProfile, on_delete=models.CASCADE, related_name='posts')
    crawl_job = models.ForeignKey(CrawlJob, on_delete=models.CASCADE, related_name='posts')
    
    # Post identifiers
    post_id = models.CharField(max_length=255, db_index=True, help_text="Platform-specific post ID")
    post_url = models.URLField()
    
    # Content
    content = models.TextField(blank=True, default='')
    media_urls = models.JSONField(default=list, blank=True, help_text="List of image/video URLs")
    media_type = models.CharField(max_length=50, blank=True, default='', help_text="photo, video, carousel, etc.")
    
    # Engagement metrics
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    shares_count = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)
    
    # Post metadata
    posted_at = models.DateTimeField(null=True, blank=True)
    language = models.CharField(max_length=10, blank=True)
    hashtags = models.JSONField(default=list, blank=True)
    mentions = models.JSONField(default=list, blank=True)
    
    # Analysis
    sentiment = models.CharField(max_length=20, blank=True, help_text="positive, negative, neutral")
    topics = models.JSONField(default=list, blank=True, help_text="Extracted topics/keywords")
    
    # Timestamps
    crawled_at = models.DateTimeField(auto_now_add=True)
    
    # Raw data
    raw_data = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-posted_at']
        unique_together = [['post_id', 'crawl_job']]
        indexes = [
            models.Index(fields=['posted_at']),
            models.Index(fields=['crawled_at']),
            models.Index(fields=['profile', 'posted_at']),
        ]
    
    def __str__(self):
        return f"{self.profile.username} - {self.post_id}"


class SocialMetrics(models.Model):
    """Aggregated metrics for profiles over time"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(SocialProfile, on_delete=models.CASCADE, related_name='metrics')
    
    # Date of metrics
    date = models.DateField(db_index=True)
    
    # Growth metrics
    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    posts_count = models.IntegerField(default=0)
    
    # Engagement metrics
    avg_likes = models.FloatField(default=0)
    avg_comments = models.FloatField(default=0)
    avg_shares = models.FloatField(default=0)
    engagement_rate = models.FloatField(default=0, help_text="Percentage")
    
    # Activity metrics
    posts_today = models.IntegerField(default=0)
    
    # Timestamps
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = [['profile', 'date']]
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['profile', 'date']),
        ]
    
    def __str__(self):
        return f"{self.profile.username} - {self.date}"


class CrawlSchedule(models.Model):
    """Schedule for recurring crawl jobs"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crawl_schedules')
    entity = models.ForeignKey(Entity, on_delete=models.SET_NULL, null=True, blank=True, related_name='crawl_schedules')
    
    # Schedule details
    name = models.CharField(max_length=255)
    platform = models.CharField(max_length=20, choices=SocialPlatform.choices)
    target_username = models.CharField(max_length=255)
    
    # Frequency
    FREQUENCY_CHOICES = [
        ('hourly', 'Every Hour'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    
    # Status
    is_active = models.BooleanField(default=True)
    last_run = models.DateTimeField(null=True, blank=True)
    next_run = models.DateTimeField(null=True, blank=True)
    
    # Configuration (same as CrawlJob)
    crawl_config = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.platform} ({self.frequency})"
