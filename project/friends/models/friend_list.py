from django.db import models
from project.utils.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _


class FriendList(TimeStampedModel):
    user = models.OneToOneField(
        "project.User",
        verbose_name=_("User"),
        related_name='friends_list',
        on_delete=models.CASCADE
    )
    friends = models.ManyToManyField(
        "project.User",
        verbose_name=_("Friends"),
        related_name='friends',
        blank=True
    )

    class Meta:
        db_table = 'friends_friend_list'
        verbose_name = _("Friend List")
        verbose_name_plural = _("Friends List")

    def __str__(self):
        return str(self.user)

    def add_friend(self, user):
        if not self.is_mutual(user):
            self.friends.add(user)

    def remove_friend(self, user):
        if self.is_mutual(user):
            self.friends.remove(user)

    def unfriend(self, friend):
        self.remove_friend(friend)
        friend.friends_list.remove_friend(self.user)

    def is_mutual(self, friend):
        if friend in self.friends.all():
            return True
        return False
