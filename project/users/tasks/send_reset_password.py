from celery import shared_task
from project.users.models import User
from django.conf import settings
from django.core.mail import send_mail
from project.utils.functions import activation_url


@shared_task
def send_reset_password_task(email):
    user = User.objects.filter(email=email).first()
    token = user.generate_reset_password_token()

    url_name = 'users:confirm-reset-password'
    subject = 'Reset Password'
    url = activation_url(url_name, token)
    message = f'Click Here for {subject} {url}'

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email,]
    )
    return 'Done'
