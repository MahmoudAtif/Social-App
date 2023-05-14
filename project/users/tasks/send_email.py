from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_email_task(subject, message, email):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email,]
    )
    return 'Done'
