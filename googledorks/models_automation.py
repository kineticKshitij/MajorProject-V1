"""
Models for Automation, Alerts, and Email Notifications
"""

from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class AutomatedDork(models.Model):
    """
    Represents a dork that runs automatically on a schedule.
    """
    SCHEDULE_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    
    dork = models.ForeignKey('GoogleDork', on_delete=models.CASCADE, related_name='automations')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='automated_dorks')
    
    # Schedule configuration
    schedule_type = models.CharField(max_length=20, choices=SCHEDULE_CHOICES, default='daily')
    schedule_time = models.TimeField(help_text="Time of day to run (e.g., 09:00)")
    is_active = models.BooleanField(default=True)
    
    # Execution tracking
    last_run = models.DateTimeField(null=True, blank=True)
    next_run = models.DateTimeField(null=True, blank=True)
    run_count = models.IntegerField(default=0)
    
    # Results tracking
    last_result_count = models.IntegerField(default=0)
    
    # Email notifications
    send_email_on_completion = models.BooleanField(default=True)
    email_recipients = models.TextField(
        help_text="Comma-separated email addresses",
        blank=True,
        default=""
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Automated Dork'
        verbose_name_plural = 'Automated Dorks'
    
    def __str__(self):
        return f"{self.dork.query} - {self.schedule_type}"
    
    def calculate_next_run(self):
        """Calculate the next run time based on schedule type."""
        if not self.last_run:
            base_time = timezone.now()
        else:
            base_time = self.last_run
        
        # Combine date with scheduled time
        next_run = base_time.replace(
            hour=self.schedule_time.hour,
            minute=self.schedule_time.minute,
            second=0,
            microsecond=0
        )
        
        # Add appropriate delta based on schedule type
        if self.schedule_type == 'daily':
            next_run += timedelta(days=1)
        elif self.schedule_type == 'weekly':
            next_run += timedelta(weeks=1)
        elif self.schedule_type == 'monthly':
            next_run += timedelta(days=30)
        
        # If next_run is in the past, move it forward
        while next_run <= timezone.now():
            if self.schedule_type == 'daily':
                next_run += timedelta(days=1)
            elif self.schedule_type == 'weekly':
                next_run += timedelta(weeks=1)
            elif self.schedule_type == 'monthly':
                next_run += timedelta(days=30)
        
        return next_run
    
    def mark_as_run(self, result_count=0):
        """Mark this automation as having been run."""
        self.last_run = timezone.now()
        self.run_count += 1
        self.last_result_count = result_count
        self.next_run = self.calculate_next_run()
        self.save()


class Alert(models.Model):
    """
    Represents an alert configuration for monitoring dork results.
    """
    TRIGGER_CHOICES = [
        ('new_results', 'New Results Found'),
        ('result_count_change', 'Result Count Changed'),
        ('keyword_found', 'Keyword Found in Results'),
        ('scheduled_report', 'Scheduled Report'),
    ]
    
    dork = models.ForeignKey('GoogleDork', on_delete=models.CASCADE, related_name='alerts')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='alerts')
    
    # Alert configuration
    name = models.CharField(max_length=200, help_text="Descriptive name for this alert")
    trigger_type = models.CharField(max_length=30, choices=TRIGGER_CHOICES)
    is_active = models.BooleanField(default=True)
    
    # Trigger conditions (stored as JSON for flexibility)
    condition_data = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional conditions for triggering (e.g., keywords, thresholds)"
    )
    
    # Notification settings
    send_email = models.BooleanField(default=True)
    email_recipients = models.TextField(
        help_text="Comma-separated email addresses",
        blank=True,
        default=""
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_triggered = models.DateTimeField(null=True, blank=True)
    trigger_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Alert'
        verbose_name_plural = 'Alerts'
    
    def __str__(self):
        return f"{self.name} - {self.get_trigger_type_display()}"
    
    def get_recipient_list(self):
        """Return list of email addresses."""
        if not self.email_recipients:
            return [self.created_by.email] if self.created_by.email else []
        return [email.strip() for email in self.email_recipients.split(',') if email.strip()]


class AlertHistory(models.Model):
    """
    Records each time an alert is triggered.
    """
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='history')
    
    # Trigger details
    triggered_at = models.DateTimeField(auto_now_add=True)
    result_count = models.IntegerField(default=0)
    new_results_count = models.IntegerField(default=0)
    
    # Notification tracking
    notification_sent = models.BooleanField(default=False)
    notification_details = models.JSONField(
        default=dict,
        blank=True,
        help_text="Details about the notification (recipients, status, errors)"
    )
    
    # Result snapshot
    result_summary = models.TextField(blank=True, help_text="Summary of results that triggered the alert")
    
    class Meta:
        ordering = ['-triggered_at']
        verbose_name = 'Alert History'
        verbose_name_plural = 'Alert Histories'
    
    def __str__(self):
        return f"{self.alert.name} - {self.triggered_at.strftime('%Y-%m-%d %H:%M')}"


class EmailTemplate(models.Model):
    """
    Email templates for different types of notifications.
    """
    TEMPLATE_CHOICES = [
        ('new_results', 'New Results Alert'),
        ('weekly_summary', 'Weekly Summary'),
        ('system_notification', 'System Notification'),
        ('test_email', 'Test Email'),
    ]
    
    name = models.CharField(max_length=100)
    template_type = models.CharField(max_length=30, choices=TEMPLATE_CHOICES)
    subject = models.CharField(max_length=200)
    html_content = models.TextField(help_text="HTML content with template variables")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['template_type', 'name']
        verbose_name = 'Email Template'
        verbose_name_plural = 'Email Templates'
    
    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"
