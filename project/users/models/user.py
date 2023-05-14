from django.db import models
from django.contrib.auth.models import AbstractUser
from project.users.managers import CustomUserManager
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _
from .secret_token import SecretToken


class User(AbstractUser):
    email = models.EmailField(
        verbose_name=_("Email Address"),
        max_length=50,
        unique=True
    )
    image = models.ImageField(
        verbose_name=_("Image"),
        upload_to='users/images',
        blank=True,
        default='users/images/defaultavatar.png'
    )
    is_guest = models.BooleanField(_("Guest"), default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users_user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email

    def deactivate(self):
        self.is_active = False
        self.save()
        return True

    def activate(self):
        self.is_active = True
        self.save()
        return True

    def generate_reset_password_token(self):
        token = SecretToken.create(
            token_type="RESET_PASSWORD",
            user=self,
            expiry_hours=1
        )
        token.deactivate_previous_tokens()
        return str(token)

    def generate_email_verivication_token(self):
        token = SecretToken.create(
            token_type="EMAIL_VERIFICATION",
            user=self,
            expiry_hours=1
        )
        token.deactivate_previous_tokens()
        return str(token)

    def get_token(self):
        token, created = Token.objects.get_or_create(user=self)
        return str(token.key)
