from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Extended User model to include Gemini API key"""
    gemini_api_key = models.CharField(
        max_length=255, 
        blank=True, 
        help_text="Your personal Google Gemini API key for AI chatbot functionality"
    )
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_email_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()
    
    def has_gemini_api_key(self):
        """Check if user has configured Gemini API key"""
        return bool(self.gemini_api_key and self.gemini_api_key.strip())


class UserProfile(models.Model):
    """Additional user profile information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    website = models.URLField(blank=True)
    github_profile = models.URLField(blank=True)
    linkedin_profile = models.URLField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    preferred_language = models.CharField(
        max_length=10,
        choices=[
            ('en', 'English'),
            ('es', 'Spanish'),
            ('fr', 'French'),
            ('de', 'German'),
            ('zh', 'Chinese'),
        ],
        default='en'
    )
    timezone = models.CharField(max_length=50, default='UTC')
    receive_notifications = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"