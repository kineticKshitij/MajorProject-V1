"""
Services package for Google Dorks application.
Contains business logic for email, alerts, and automation.
"""

from .email_service import EmailService
from .alert_service import AlertEngine

__all__ = ['EmailService', 'AlertEngine']
