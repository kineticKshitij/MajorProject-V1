"""
Management command to trigger test alert for demonstration.
Usage: python manage.py trigger_test_alert --email your@email.com
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from googledorks.services import EmailService, AlertEngine
from googledorks.models import GoogleDork, SearchResult
from googledorks.models_automation import Alert, AlertHistory


class Command(BaseCommand):
    help = 'Trigger a test alert for demonstration purposes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email address to send test alert to',
            required=True
        )
        parser.add_argument(
            '--dork-id',
            type=int,
            help='Dork ID to use (optional, will create demo alert if not provided)',
            default=None
        )

    def handle(self, *args, **options):
        email = options['email']
        dork_id = options.get('dork_id')
        
        self.stdout.write(self.style.SUCCESS('Starting test alert demonstration...'))
        
        try:
            # Get or create a demo dork
            if dork_id:
                dork = GoogleDork.objects.get(id=dork_id)
            else:
                dork = GoogleDork.objects.first()
                if not dork:
                    self.stdout.write(self.style.ERROR('No dorks found in database. Please create one first.'))
                    return
            
            self.stdout.write(f'Using dork: "{dork.title}" (ID: {dork.id})')
            
            # Create or get demo alert
            alert, created = Alert.objects.get_or_create(
                dork=dork,
                name='Demo Test Alert',
                defaults={
                    'trigger_type': 'new_results',
                    'send_email': True,
                    'email_recipients': email,
                    'is_active': True,
                    'created_by_id': 1  # Assumes admin user exists
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created new demo alert (ID: {alert.id})'))
            else:
                alert.email_recipients = email
                alert.save()
                self.stdout.write(f'Using existing demo alert (ID: {alert.id})')
            
            # Create demo results
            demo_results = [
                SearchResult(
                    dork=dork,
                    title=f'Demo Result {i+1}: Sensitive Information Exposed',
                    url=f'https://example{i+1}.com/exposed-data',
                    snippet=f'This is a demo result showing potential data exposure. Found keywords: password, admin, config. This result was generated for demonstration purposes.',
                    domain=f'example{i+1}.com',
                    is_interesting=True
                )
                for i in range(3)
            ]
            
            self.stdout.write('Creating demo search results...')
            
            # Trigger the alert manually
            alert_history = AlertHistory.objects.create(
                alert=alert,
                result_count=len(demo_results),
                new_results_count=len(demo_results),
                result_summary='Demo results for testing alert system',
                notification_sent=False
            )
            
            # Send notification
            results_preview = [
                {
                    'title': result.title,
                    'url': result.url,
                    'snippet': result.snippet
                }
                for result in demo_results
            ]
            
            self.stdout.write(f'Sending test alert email to: {email}')
            
            success = EmailService.send_new_results_notification(
                alert_name=alert.name,
                dork_query=dork.query,
                new_results_count=len(demo_results),
                total_results=len(demo_results),
                results_preview=results_preview,
                recipients=[email],
                dork_id=dork.id
            )
            
            # Update alert history
            alert_history.notification_sent = success
            alert_history.notification_details = {
                'success': success,
                'recipients': [email],
                'sent_at': timezone.now().isoformat(),
                'test_mode': True
            }
            alert_history.save()
            
            # Update alert stats
            alert.last_triggered = timezone.now()
            alert.trigger_count += 1
            alert.save()
            
            if success:
                self.stdout.write(self.style.SUCCESS('✅ Test alert sent successfully!'))
                self.stdout.write(f'Check your email: {email}')
                self.stdout.write(f'Alert History ID: {alert_history.id}')
            else:
                self.stdout.write(self.style.ERROR('❌ Failed to send test alert email'))
                self.stdout.write('Check your email configuration in settings.py')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
            import traceback
            self.stdout.write(traceback.format_exc())
