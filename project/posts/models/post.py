from django.db import models
from django.utils.translation import gettext_lazy as _
from project.utils.models import TimeStampedModel
from project.posts.managers import PostManager


class Post(TimeStampedModel):

    class PrivacyEnum(models.IntegerChoices):
        PUBLIC = 1, _('Public')
        PRIVATE = 2, _('Private')
        FRIENDS = 3, _('Friends')

    user = models.ForeignKey(
        "project.User",
        verbose_name=_("User"),
        related_name='posts',
        on_delete=models.CASCADE
    )
    content = models.TextField(
        max_length=200,
        null=True,
        blank=True
    )
    image = models.FileField(
        verbose_name=_("Image"),
        upload_to='posts/images/',
        null=True,
        blank=True
    )
    likes = models.ManyToManyField(
        "project.User",
        verbose_name=_("Likes"),
        blank=True,
        related_name='likes'
    )
    tags = models.ManyToManyField(
        "project.User",
        verbose_name=_("Tags"),
        blank=True,
        related_name='tags'
    )
    privacy = models.IntegerField(
        choices=PrivacyEnum.choices,
        default=PrivacyEnum.PUBLIC
    )
    is_published = models.BooleanField(default=True)
    is_drafted = models.BooleanField(default=False)

    objects = PostManager()

    class Meta:
        db_table = 'posts_post'
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ['-created_at']

    def __str__(self):
        return str(self.user)

    def is_public(self):
        return self.privacy == self.PrivacyEnum.PUBLIC

    def is_private(self):
        return self.privacy == self.PrivacyEnum.PRIVATE

    def is_friends(self):
        return self.privacy == self.PrivacyEnum.FRIENDS

    def like(self, user):
        if not user in self.likes.all():
            self.likes.add(user)

    def unlike(self, user):
        if user in self.likes.all():
            self.likes.remove(user)
