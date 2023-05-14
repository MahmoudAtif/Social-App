from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from project.users.models import User, SendEmail


@receiver(post_save, sender=User)
def send_email_verification_receiver(sender, instance, created, **kwargs):
    if not instance.is_active:
        SendEmail.objects.create(
            email_type='EMAIL_VERIFICATION',
            email=instance.email
        )
    return True
