from django.db import models
from django.utils.translation import gettext_lazy as _
from project.utils.models import TimeStampedModel
from project.users.models import User
from project.users.tasks import send_email_task, send_email_verification_task, send_reset_password_task


class SendEmail(TimeStampedModel):

    class EmailTypes(models.TextChoices):
        RESET_PASSWORD = "RESET_PASSWORD", _("Reset Password")
        EMAIL_VERIFICATION = "EMAIL_VERIFICATION", _("Email Verification")
        REGULAR_EMAIL = "REGULAR_EMAIL", _('Regular Email')

    email_type = models.CharField(
        choices=EmailTypes.choices,
        max_length=20,
        default=EmailTypes.EMAIL_VERIFICATION,
        verbose_name=_("Email Type"),
    )
    email = models.EmailField(_('Email Address'), max_length=250)
    subject = models.CharField(
        verbose_name=_('Subject'),
        null=True,
        blank=True,
        max_length=100
    )
    message = models.TextField(
        verbose_name=_('Message'),
        null=True,
        blank=True,
        max_length=200
    )

    class Meta:
        db_table = "auth_send_email"
        verbose_name = _("Send Email")
        verbose_name_plural = _("Send Emails")

    def __str__(self):
        return f'{self.email} - {self.email_type}'

    def get_user(self):
        user = User.objects.filter(email=self.email).first()
        return user

    def send_email_verification(self):
        user = self.get_user()
        if user is not None and not user.is_active:
            send_email_verification_task.delay(
                email=self.email
            )
        return None

    def send_reset_password(self):
        user = self.get_user()
        if user is not None:
            send_reset_password_task.delay(
                email=self.email
            )
        return None

    def send_regular_email(self):
        user = self.get_user()
        send_email_task.delay(
            self.subject,
            self.message,
            user.email
        )
        return True
