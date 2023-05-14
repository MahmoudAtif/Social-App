from django.db import models
from django.utils.translation import gettext_lazy as _
from project.utils.models import TimeStampedModel


class Share(TimeStampedModel):
    user = models.ForeignKey(
        "project.User",
        verbose_name=_("User"),
        related_name='shares',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        "project.Post",
        verbose_name=_("User"),
        related_name='shares',
        on_delete=models.CASCADE
    )
    content = models.TextField(
        max_length=200,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'posts_share'
        verbose_name = _("Share")
        verbose_name_plural = _("Shares")
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} - {self.post}'
