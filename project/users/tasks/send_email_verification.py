from celery import shared_task
from project.users.models import User
from django.conf import settings
from django.core.mail import send_mail
from project.utils.functions import activation_url


@shared_task
def send_email_verification_task(email):
    user = User.objects.filter(email=email).first()
    token = user.generate_email_verivication_token()

    url_name = 'users:email-verification'
    url = activation_url(url_name, token)
    subject = 'Email Activation'
    message = f'Click Here for {subject} {url}'

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email,]
    )
    return 'Done'
