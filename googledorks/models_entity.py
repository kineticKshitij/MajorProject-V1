"""
Entity-focused models for targeted information gathering
This module extends the Google Dorks Toolkit to support specific entity research
"""

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.core.validators import URLValidator
import uuid


class EntityType(models.Model):
    """Types of entities that can be researched"""
    ENTITY_TYPES = [
        ('company', 'Company'),
        ('person', 'Person'),
        ('organization', 'Organization'),
        ('government', 'Government Agency'),
        ('educational', 'Educational Institution'),
        ('domain', 'Domain/Website'),
        ('project', 'Project/Initiative'),
        ('event', 'Event/Conference'),
    ]
    
    name = models.CharField(max_length=50, choices=ENTITY_TYPES, unique=True)
    display_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='bi-building', help_text="Bootstrap icon class")
    color = models.CharField(max_length=7, default='#007bff', help_text="Hex color code")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['display_name']
        verbose_name = "Entity Type"
        verbose_name_plural = "Entity Types"
    
    def __str__(self):
        return self.display_name


class Entity(models.Model):
    """Core entity model for companies, persons, organizations, etc."""
    PRIORITY_LEVELS = [
        ('low', 'Low Priority'),
        ('medium', 'Medium Priority'),
        ('high', 'High Priority'),
        ('critical', 'Critical Priority'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active Research'),
        ('completed', 'Research Completed'),
        ('on_hold', 'On Hold'),
        ('archived', 'Archived'),
    ]
    
    # Core identification
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, help_text="Primary name of the entity")
    entity_type = models.ForeignKey(EntityType, on_delete=models.CASCADE, related_name='entities')
    aliases = models.JSONField(default=list, blank=True, help_text="Alternative names, acronyms, etc.")
    
    # Basic information
    description = models.TextField(blank=True, help_text="Brief description of the entity")
    industry = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=200, blank=True, help_text="Primary location/headquarters")
    founded_date = models.DateField(null=True, blank=True)
    
    # Online presence
    website = models.URLField(blank=True)
    domains = models.JSONField(default=list, blank=True, help_text="Known domains associated with entity")
    social_media = models.JSONField(default=dict, blank=True, help_text="Social media profiles")
    
    # Research metadata
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    tags = models.JSONField(default=list, blank=True, help_text="Custom tags for categorization")
    
    # Tracking
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_entities')
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='assigned_entities')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_researched = models.DateTimeField(null=True, blank=True)
    
    # Statistics
    search_count = models.PositiveIntegerField(default=0)
    results_found = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-updated_at']
        verbose_name = "Entity"
        verbose_name_plural = "Entities"
        
    def __str__(self):
        return f"{self.name} ({self.entity_type.display_name})"
    
    def get_absolute_url(self):
        return reverse('googledorks:entity_detail', kwargs={'pk': self.pk})
    
    def increment_search_count(self):
        """Increment search count and update last researched timestamp"""
        self.search_count += 1
        self.last_researched = timezone.now()
        self.save(update_fields=['search_count', 'last_researched'])
    
    def get_all_names(self):
        """Get all possible names including aliases"""
        names = [self.name]
        if self.aliases:
            names.extend(self.aliases)
        return names
    
    def get_domain_list(self):
        """Get list of domains as strings"""
        return self.domains if self.domains else []
    
    def add_domain(self, domain):
        """Add a domain to the entity"""
        if not self.domains:
            self.domains = []
        if domain not in self.domains:
            self.domains.append(domain)
            self.save(update_fields=['domains'])
    
    def get_social_media_links(self):
        """Get formatted social media links"""
        if not self.social_media:
            return {}
        
        formatted = {}
        for platform, handle in self.social_media.items():
            if handle:
                if platform.lower() == 'twitter':
                    formatted[platform] = f"https://twitter.com/{handle.lstrip('@')}"
                elif platform.lower() == 'linkedin':
                    formatted[platform] = f"https://linkedin.com/company/{handle}"
                elif platform.lower() == 'facebook':
                    formatted[platform] = f"https://facebook.com/{handle}"
                elif platform.lower() == 'instagram':
                    formatted[platform] = f"https://instagram.com/{handle.lstrip('@')}"
                else:
                    formatted[platform] = handle
        return formatted


class EntityAttribute(models.Model):
    """Flexible attributes for entities (key-value pairs)"""
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='attributes')
    key = models.CharField(max_length=100, help_text="Attribute name (e.g., 'CEO', 'Stock Symbol', 'Employee Count')")
    value = models.TextField(help_text="Attribute value")
    value_type = models.CharField(
        max_length=20,
        choices=[
            ('text', 'Text'),
            ('number', 'Number'),
            ('date', 'Date'),
            ('url', 'URL'),
            ('email', 'Email'),
            ('phone', 'Phone'),
        ],
        default='text'
    )
    is_public = models.BooleanField(default=True, help_text="Whether this attribute should be publicly visible")
    source = models.CharField(max_length=200, blank=True, help_text="Source of this information")
    confidence = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low Confidence'),
            ('medium', 'Medium Confidence'),
            ('high', 'High Confidence'),
            ('verified', 'Verified'),
        ],
        default='medium'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['key', '-updated_at']
        unique_together = ['entity', 'key']
        verbose_name = "Entity Attribute"
        verbose_name_plural = "Entity Attributes"
    
    def __str__(self):
        return f"{self.entity.name} - {self.key}: {self.value}"


class EntitySearchTemplate(models.Model):
    """Predefined search templates for different entity types"""
    entity_type = models.ForeignKey(EntityType, on_delete=models.CASCADE, related_name='search_templates')
    name = models.CharField(max_length=100, help_text="Template name")
    description = models.TextField(help_text="What this template searches for")
    query_template = models.TextField(help_text="Dork query with placeholders like {entity_name}, {domain}")
    category = models.CharField(
        max_length=50,
        choices=[
            ('basic_info', 'Basic Information'),
            ('contact_info', 'Contact Information'),
            ('employees', 'Employee Information'),
            ('financials', 'Financial Information'),
            ('vulnerabilities', 'Security Vulnerabilities'),
            ('documents', 'Document Discovery'),
            ('social_media', 'Social Media Presence'),
            ('partnerships', 'Partnerships & Relations'),
            ('news', 'News & Press'),
            ('infrastructure', 'Technical Infrastructure'),
        ],
        default='basic_info'
    )
    risk_level = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low Risk'),
            ('medium', 'Medium Risk'),
            ('high', 'High Risk'),
            ('critical', 'Critical Risk'),
        ],
        default='low'
    )
    difficulty = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ],
        default='beginner'
    )
    is_active = models.BooleanField(default=True)
    usage_count = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['entity_type', 'category', 'name']
        verbose_name = "Entity Search Template"
        verbose_name_plural = "Entity Search Templates"
    
    def __str__(self):
        return f"{self.entity_type.display_name} - {self.name}"
    
    def generate_query(self, entity, **kwargs):
        """Generate a query for a specific entity"""
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
            return self.query_template.format(**context)
        except KeyError as e:
            return f"Template error: Missing placeholder {e}"
    
    def increment_usage(self):
        """Increment usage count"""
        self.usage_count += 1
        self.save(update_fields=['usage_count'])


class EntitySearchSession(models.Model):
    """Search sessions focused on specific entities"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='search_sessions')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    search_templates = models.ManyToManyField(EntitySearchTemplate, blank=True, related_name='sessions')
    
    # Session configuration
    auto_execute = models.BooleanField(default=False, help_text="Automatically execute all templates")
    save_results = models.BooleanField(default=True, help_text="Save search results")
    notify_completion = models.BooleanField(default=False, help_text="Notify when session completes")
    
    # Tracking
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Statistics
    total_searches = models.PositiveIntegerField(default=0)
    total_results = models.PositiveIntegerField(default=0)
    interesting_results = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Entity Search Session"
        verbose_name_plural = "Entity Search Sessions"
    
    def __str__(self):
        return f"{self.name} - {self.entity.name}"
    
    def get_absolute_url(self):
        return reverse('googledorks:entity_session_detail', kwargs={'pk': self.pk})
    
    def start_session(self):
        """Mark session as started"""
        self.started_at = timezone.now()
        self.save(update_fields=['started_at'])
    
    def complete_session(self):
        """Mark session as completed"""
        self.completed_at = timezone.now()
        self.save(update_fields=['completed_at'])
    
    def is_active(self):
        """Check if session is currently active"""
        return self.started_at and not self.completed_at
    
    def is_completed(self):
        """Check if session is completed"""
        return bool(self.completed_at)
    
    def get_progress_percentage(self):
        """Calculate completion percentage"""
        if not self.search_templates.exists():
            return 0
        
        total_templates = self.search_templates.count()
        if total_templates == 0:
            return 0
        
        # This would need to be calculated based on actual execution
        # For now, return based on completion status
        return 100 if self.is_completed() else 0


class EntitySearchResult(models.Model):
    """Search results specific to entities"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='search_results')
    session = models.ForeignKey(EntitySearchSession, on_delete=models.CASCADE, null=True, blank=True, related_name='results')
    template = models.ForeignKey(EntitySearchTemplate, on_delete=models.CASCADE, related_name='results')
    
    # Result data
    title = models.CharField(max_length=500)
    url = models.URLField(max_length=2000)
    snippet = models.TextField(blank=True)
    domain = models.CharField(max_length=200, blank=True)
    
    # Classification
    relevance_score = models.FloatField(default=0.0, help_text="AI-calculated relevance score")
    is_interesting = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    contains_sensitive_info = models.BooleanField(default=False)
    
    # Analysis
    extracted_info = models.JSONField(default=dict, blank=True, help_text="Extracted structured information")
    tags = models.JSONField(default=list, blank=True)
    notes = models.TextField(blank=True)
    
    # Tracking
    found_at = models.DateTimeField(auto_now_add=True)
    last_verified = models.DateTimeField(null=True, blank=True)
    verification_status = models.CharField(
        max_length=20,
        choices=[
            ('not_checked', 'Not Checked'),
            ('accessible', 'Accessible'),
            ('requires_auth', 'Requires Authentication'),
            ('not_found', 'Not Found'),
            ('blocked', 'Access Blocked'),
        ],
        default='not_checked'
    )
    
    class Meta:
        ordering = ['-found_at']
        unique_together = ['entity', 'url']
        verbose_name = "Entity Search Result"
        verbose_name_plural = "Entity Search Results"
    
    def __str__(self):
        return f"{self.entity.name} - {self.title[:50]}..."
    
    def save(self, *args, **kwargs):
        # Extract domain from URL
        if self.url and not self.domain:
            from urllib.parse import urlparse
            parsed_url = urlparse(self.url)
            self.domain = parsed_url.netloc
        
        super().save(*args, **kwargs)
    
    def mark_as_interesting(self):
        """Mark result as interesting"""
        self.is_interesting = True
        self.save(update_fields=['is_interesting'])
    
    def verify_accessibility(self):
        """Check if the URL is still accessible (placeholder for implementation)"""
        # This would contain logic to verify URL accessibility
        self.last_verified = timezone.now()
        # Implementation would set verification_status based on actual check
        self.save(update_fields=['last_verified', 'verification_status'])


class EntityRelationship(models.Model):
    """Relationships between entities"""
    RELATIONSHIP_TYPES = [
        ('parent_company', 'Parent Company'),
        ('subsidiary', 'Subsidiary'),
        ('partner', 'Business Partner'),
        ('competitor', 'Competitor'),
        ('supplier', 'Supplier'),
        ('customer', 'Customer'),
        ('employee', 'Employee'),
        ('founder', 'Founder'),
        ('investor', 'Investor'),
        ('acquired_by', 'Acquired By'),
        ('acquired', 'Acquired'),
        ('related', 'Related Entity'),
    ]
    
    from_entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='relationships_from')
    to_entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='relationships_to')
    relationship_type = models.CharField(max_length=50, choices=RELATIONSHIP_TYPES)
    description = models.TextField(blank=True)
    confidence = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low Confidence'),
            ('medium', 'Medium Confidence'),
            ('high', 'High Confidence'),
            ('verified', 'Verified'),
        ],
        default='medium'
    )
    source = models.CharField(max_length=200, blank=True, help_text="Source of this relationship info")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['from_entity', 'to_entity', 'relationship_type']
        verbose_name = "Entity Relationship"
        verbose_name_plural = "Entity Relationships"
    
    def __str__(self):
        return f"{self.from_entity.name} -> {self.get_relationship_type_display()} -> {self.to_entity.name}"


class EntityNote(models.Model):
    """Notes and observations about entities"""
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=200)
    content = models.TextField()
    note_type = models.CharField(
        max_length=20,
        choices=[
            ('observation', 'Observation'),
            ('finding', 'Research Finding'),
            ('hypothesis', 'Hypothesis'),
            ('todo', 'To Do'),
            ('warning', 'Warning'),
            ('contact', 'Contact Information'),
        ],
        default='observation'
    )
    priority = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('critical', 'Critical'),
        ],
        default='medium'
    )
    tags = models.JSONField(default=list, blank=True)
    is_private = models.BooleanField(default=False, help_text="Private to creator only")
    
    # Tracking
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Entity Note"
        verbose_name_plural = "Entity Notes"
    
    def __str__(self):
        return f"{self.entity.name} - {self.title}"