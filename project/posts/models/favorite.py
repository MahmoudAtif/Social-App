from django.db import models
from project.utils.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _


class Favorite(TimeStampedModel):
    user = models.OneToOneField(
        "project.User",
        verbose_name=_("User"),
        related_name='favorite',
        on_delete=models.CASCADE
    )
    posts = models.ManyToManyField(
        "project.Post",
        verbose_name=_("Posts"),
        related_name='favorites'
    )

    class Meta:
        db_table = 'posts_favorite'
        verbose_name = _('Favorite')
        verbose_name_plural = _('Favorites')

    def __str__(self):
        return str(self.user)

    def add_favorite(self, post):
        if not post in self.posts.all():
            self.posts.add(post)
    
    def remove_favorite(self, post):
        if post in self.posts.all():
            self.posts.remove(post)