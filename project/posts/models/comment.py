from django.db import models
from project.utils.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _


class Comment(TimeStampedModel):
    user = models.ForeignKey(
        "project.User",
        verbose_name=_("User"),
        related_name='comments',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        "project.Post",
        verbose_name=_("Post"),
        related_name='comments',
        on_delete=models.CASCADE
    )
    comment = models.TextField(max_length=200)
    likes = models.ManyToManyField(
        "project.User",
        verbose_name=_("Likes"),
        blank=True,
        related_name='comment_likes'
    )

    class Meta:
        db_table = 'posts_comment'
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __str__(self):
        return f'{self.user} - {self.post}'

    def like(self, user):
        if not user in self.likes.all():
            self.likes.add(user)

    def unlike(self, user):
        if user in self.likes.all():
            self.likes.remove(user)
