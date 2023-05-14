import os
import binascii
from django.db import models
from datetime import timedelta
from django.utils import timezone
from project.utils.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _


class SecretToken(TimeStampedModel):
    """SecretToken model"""

    class TokenTypes(models.TextChoices):
        RESET_PASSWORD = "RESET_PASSWORD", _("Reset Password")
        EMAIL_VERIFICATION = "EMAIL_VERIFICATION", _("Email Verification")

    key = models.CharField(
        blank=True, max_length=100,
        db_index=True,
        verbose_name=_("Key")
    )
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Expires At"),
    )
    lifetime = models.BooleanField(default=False)
    token_type = models.CharField(
        choices=TokenTypes.choices,
        max_length=20,
        default=TokenTypes.RESET_PASSWORD,
        verbose_name=_("Token Type"),
    )
    user = models.ForeignKey(
        "project.User",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    class Meta:
        db_table = "auth_secret_token"
        verbose_name = _("Secret Token")
        verbose_name_plural = _("Secret Tokens")

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(SecretToken, self).save(*args, **kwargs)

    def deactivate_previous_tokens(self):
        return (
            self.__class__.objects.filter(
                user=self.user,
                token_type=self.token_type,
            )
            .exclude(
                id=self.id,
            )
            .update(
                is_active=False,
            )
        )

    def deactivate(self):
        self.is_active = False
        self.save()
        return True

    @property
    def masked_key(self):
        value = None
        if self.key:
            value = "{0}*****{1}".format(self.key[:10], self.key[-10:])
        return value

    def generate_key(self):
        prefix = ""
        secret_key = binascii.hexlify(os.urandom(20)).decode()
        prefix = self.token_type.replace(" ", "_").lower()
        return "%s_%s" % (prefix, secret_key)

    @property
    def is_expired(self):
        if not self.is_active:
            return True

        if self.lifetime:
            return False

        if self.expires_at > timezone.now():
            return False

        return True

    @classmethod
    def create(cls, token_type, user, expiry_hours=None, lifetime=False):
        if token_type not in cls.TokenTypes.values:
            return None

        if not isinstance(expiry_hours, int) and not lifetime:
            return None

        expiry_time = timezone.now() + timedelta(hours=expiry_hours)
        return cls.objects.create(
            token_type=token_type,
            user=user,
            expires_at=expiry_time,
            lifetime=lifetime,
        )
