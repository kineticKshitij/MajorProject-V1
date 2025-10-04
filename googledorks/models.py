from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

# Import entity models
from .models_entity import (
    EntityType, Entity, EntityAttribute, EntitySearchTemplate,
    EntitySearchSession, EntitySearchResult, EntityRelationship, EntityNote
)


class DorkCategory(models.Model):
    """Categories for organizing Google dorks"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#007bff', help_text="Hex color code for category")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Dork Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_dork_count(self):
        return self.dorks.count()


class GoogleDork(models.Model):
    """Google dork queries"""
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    RISK_LEVELS = [
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
        ('critical', 'Critical Risk'),
    ]

    title = models.CharField(max_length=200)
    query = models.TextField(help_text="The actual Google dork query")
    description = models.TextField()
    category = models.ForeignKey(DorkCategory, on_delete=models.CASCADE, related_name='dorks')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    risk_level = models.CharField(max_length=20, choices=RISK_LEVELS, default='low')
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    is_active = models.BooleanField(default=True)
    
    # Entity support
    supports_entities = models.BooleanField(default=False, help_text="Whether this dork can be used with entity placeholders")
    entity_placeholders = models.JSONField(default=list, blank=True, help_text="Available placeholders like {entity_name}, {domain}")
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    usage_count = models.PositiveIntegerField(default=0)
    execution_count = models.PositiveIntegerField(default=0, help_text="Number of times this dork has been executed")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('googledorks:dork_detail', kwargs={'pk': self.pk})

    def increment_usage(self):
        self.usage_count += 1
        self.save(update_fields=['usage_count'])

    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def generate_entity_query(self, entity, **kwargs):
        """Generate entity-specific query if this dork supports entities"""
        if not self.supports_entities:
            return self.query
            
        context = {
            'entity_name': entity.name,
            'domain': entity.website.replace('https://', '').replace('http://', '').replace('www.', '') if entity.website else '',
            'location': entity.location,
            'industry': entity.industry,
            **kwargs
        }
        
        # Add all aliases as potential substitutions
        for i, alias in enumerate(entity.get_all_names()):
            context[f'alias_{i}'] = alias
        
        # Add domains
        for i, domain in enumerate(entity.get_domain_list()):
            context[f'domain_{i}'] = domain
            
        try:
            return self.query.format(**context)
        except KeyError as e:
            return self.query  # Return original if template error


class SearchResult(models.Model):
    """Results from executing Google dorks"""
    dork = models.ForeignKey(GoogleDork, on_delete=models.CASCADE, related_name='results')
    entity = models.ForeignKey('Entity', on_delete=models.CASCADE, null=True, blank=True, related_name='dork_results', help_text="Associated entity if this is entity-specific search")
    title = models.CharField(max_length=500)
    url = models.URLField(max_length=2000)
    snippet = models.TextField(blank=True)
    domain = models.CharField(max_length=200, blank=True)
    search_date = models.DateTimeField(auto_now_add=True)
    is_interesting = models.BooleanField(default=False, help_text="Mark as interesting for review")
    notes = models.TextField(blank=True)
    screenshot_path = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ['-search_date']
        unique_together = ['dork', 'url']  # Prevent duplicate results

    def __str__(self):
        return f"{self.title} - {self.domain}"

    def save(self, *args, **kwargs):
        if self.url and not self.domain:
            from urllib.parse import urlparse
            parsed_url = urlparse(self.url)
            self.domain = parsed_url.netloc
        super().save(*args, **kwargs)


class SearchSession(models.Model):
    """Track search sessions for analysis"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    dorks = models.ManyToManyField(GoogleDork, related_name='sessions')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    total_results = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def mark_completed(self):
        self.completed_at = timezone.now()
        self.save(update_fields=['completed_at'])

    def is_completed(self):
        return self.completed_at is not None


class DorkBookmark(models.Model):
    """User bookmarks for favorite dorks"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dork = models.ForeignKey(GoogleDork, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['user', 'dork']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.dork.title}"
