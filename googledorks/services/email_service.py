"""
Email Service for sending notifications and alerts.
Handles email rendering, sending, and tracking.
"""

from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """
    Service for handling all email operations in the application.
    """
    
    @staticmethod
    def send_alert_email(
        recipients: List[str],
        subject: str,
        context: Dict,
        template_name: str = 'new_results_alert'
    ) -> bool:
        """
        Send an alert email using HTML template.
        
        Args:
            recipients: List of email addresses
            subject: Email subject line
            context: Template context variables
            template_name: Name of the template to use
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Add default context variables
            context.update({
                'site_name': 'AI-Enhanced Google Dorks Toolkit',
                'site_url': settings.FRONTEND_URL if hasattr(settings, 'FRONTEND_URL') else 'http://localhost:3000',
                'current_year': timezone.now().year,
            })
            
            # Render HTML content
            html_content = render_to_string(
                f'emails/{template_name}.html',
                context
            )
            
            # Create plain text version (strip HTML)
            from html.parser import HTMLParser
            
            class HTMLTextExtractor(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.text = []
                
                def handle_data(self, data):
                    self.text.append(data)
                
                def get_text(self):
                    return ''.join(self.text)
            
            parser = HTMLTextExtractor()
            parser.feed(html_content)
            text_content = parser.get_text()
            
            # Send email
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=recipients,
            )
            email.attach_alternative(html_content, "text/html")
            email.send(fail_silently=False)
            
            logger.info(f"Email sent successfully to {', '.join(recipients)}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False
    
    @staticmethod
    def send_new_results_notification(
        alert_name: str,
        dork_query: str,
        new_results_count: int,
        total_results: int,
        results_preview: List[Dict],
        recipients: List[str],
        dork_id: Optional[int] = None
    ) -> bool:
        """
        Send notification about new dork results.
        
        Args:
            alert_name: Name of the alert
            dork_query: The dork query that was executed
            new_results_count: Number of new results found
            total_results: Total number of results
            results_preview: List of result dicts with title, url, snippet
            recipients: Email recipients
            dork_id: Optional dork ID for linking
            
        Returns:
            bool: Success status
        """
        subject = f"🔔 New Results: {alert_name}"
        
        context = {
            'alert_name': alert_name,
            'dork_query': dork_query,
            'new_results_count': new_results_count,
            'total_results': total_results,
            'results_preview': results_preview[:5],  # Show top 5
            'has_more': len(results_preview) > 5,
            'remaining_count': len(results_preview) - 5 if len(results_preview) > 5 else 0,
            'dork_id': dork_id,
            'timestamp': timezone.now(),
        }
        
        return EmailService.send_alert_email(
            recipients=recipients,
            subject=subject,
            context=context,
            template_name='new_results_alert'
        )
    
    @staticmethod
    def send_weekly_summary(
        user_email: str,
        summary_data: Dict,
    ) -> bool:
        """
        Send weekly summary report.
        
        Args:
            user_email: Recipient email
            summary_data: Dict containing:
                - total_searches: int
                - total_results: int
                - top_dorks: List[Dict]
                - recent_alerts: List[Dict]
                - period_start: datetime
                - period_end: datetime
                
        Returns:
            bool: Success status
        """
        subject = f"📊 Weekly Summary Report - {summary_data.get('period_start', timezone.now()).strftime('%B %d, %Y')}"
        
        context = {
            'user_name': user_email.split('@')[0].title(),
            'summary': summary_data,
        }
        
        return EmailService.send_alert_email(
            recipients=[user_email],
            subject=subject,
            context=context,
            template_name='weekly_summary'
        )
    
    @staticmethod
    def send_automation_complete(
        automation_name: str,
        dork_query: str,
        result_count: int,
        execution_time: float,
        recipients: List[str],
        errors: Optional[List[str]] = None
    ) -> bool:
        """
        Send notification when automated dork execution completes.
        
        Args:
            automation_name: Name of the automation
            dork_query: Query that was executed
            result_count: Number of results found
            execution_time: Time taken in seconds
            recipients: Email recipients
            errors: Optional list of error messages
            
        Returns:
            bool: Success status
        """
        status = "⚠️ Completed with Errors" if errors else "✅ Successfully Completed"
        subject = f"{status}: {automation_name}"
        
        context = {
            'automation_name': automation_name,
            'dork_query': dork_query,
            'result_count': result_count,
            'execution_time': round(execution_time, 2),
            'has_errors': bool(errors),
            'errors': errors or [],
            'timestamp': timezone.now(),
        }
        
        return EmailService.send_alert_email(
            recipients=recipients,
            subject=subject,
            context=context,
            template_name='automation_complete'
        )
    
    @staticmethod
    def send_test_email(recipient: str) -> bool:
        """
        Send a test email to verify email configuration.
        
        Args:
            recipient: Email address to send test to
            
        Returns:
            bool: Success status
        """
        subject = "✅ Test Email - AI-Enhanced Google Dorks Toolkit"
        
        context = {
            'test_message': 'If you are receiving this email, your email configuration is working correctly!',
            'timestamp': timezone.now(),
        }
        
        return EmailService.send_alert_email(
            recipients=[recipient],
            subject=subject,
            context=context,
            template_name='test_email'
        )
