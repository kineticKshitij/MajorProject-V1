"""
Management command to test email configuration.
Usage: python manage.py test_email --email your@email.com
"""

from django.core.management.base import BaseCommand
from googledorks.services import EmailService


class Command(BaseCommand):
    help = 'Send a test email to verify email configuration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email address to send test email to',
            required=True
        )

    def handle(self, *args, **options):
        email = options['email']
        
        self.stdout.write(self.style.SUCCESS('Testing email configuration...'))
        
        try:
            success = EmailService.send_test_email(email)
            
            if success:
                self.stdout.write(self.style.SUCCESS('✅ Test email sent successfully!'))
                self.stdout.write(f'Check your inbox: {email}')
                self.stdout.write('')
                self.stdout.write('If you see the email in the console above:')
                self.stdout.write('  → You are in DEBUG mode (console backend)')
                self.stdout.write('  → Set DEBUG=False and configure SMTP to send real emails')
            else:
                self.stdout.write(self.style.ERROR('❌ Failed to send test email'))
                self.stdout.write('Check your email configuration in settings.py')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
            import traceback
            self.stdout.write(traceback.format_exc())
