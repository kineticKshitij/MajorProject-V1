from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile when a User is created"""
    if created:
        try:
            # Check if profile already exists (shouldn't happen, but just in case)
            if not hasattr(instance, 'profile'):
                UserProfile.objects.create(user=instance)
                logger.info(f"Created UserProfile for user: {instance.username}")
        except Exception as e:
            logger.error(f"Error creating UserProfile for user {instance.username}: {e}")


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the UserProfile when the User is saved"""
    try:
        if hasattr(instance, 'profile'):
            instance.profile.save()
    except UserProfile.DoesNotExist:
        # If profile doesn't exist, create it
        try:
            UserProfile.objects.create(user=instance)
            logger.info(f"Created missing UserProfile for user: {instance.username}")
        except Exception as e:
            logger.error(f"Error creating missing UserProfile for user {instance.username}: {e}")
    except Exception as e:
        logger.error(f"Error saving UserProfile for user {instance.username}: {e}")