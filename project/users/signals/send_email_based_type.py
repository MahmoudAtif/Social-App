from django.dispatch import receiver
from django.db.models.signals import pre_save
from project.users.models import SendEmail
from django.core import exceptions


@receiver(pre_save, sender=SendEmail)
def send_email_based_type_receiver(sender, instance, **kwargs):
    if instance.email_type == 'RESET_PASSWORD':
        return instance.send_reset_password()

    elif instance.email_type == 'REGULAR_EMAIL':
        if not instance.subject and not instance.message:
            raise exceptions.ValidationError(
                "can't save without subject and message"
            )
        return instance.send_regular_email()

    else:
        return instance.send_email_verification()
