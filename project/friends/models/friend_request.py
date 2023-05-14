from django.db import models
from project.utils.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from project.friends.models import FriendList


class FriendRequest(TimeStampedModel):
    sender = models.ForeignKey(
        "project.User",
        verbose_name=_("Sender"),
        related_name='sender',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        "project.User",
        verbose_name=_("Receiver"),
        related_name='receiver',
        on_delete=models.CASCADE
    )
    is_active = models.BooleanField(verbose_name=_("Active"), default=True)

    class Meta:
        db_table = 'friends_friend_request'
        verbose_name = _("Friend Request")
        verbose_name_plural = _("Friend Requests")

    def __str__(self):
        return str(self.sender)

    def accept(self):
        # get friend_list for a reveiver and add the sender to a friend list
        receiver_friends_list, created = FriendList.objects.get_or_create(
            user=self.receiver
        )
        receiver_friends_list.add_friend(self.sender)

        sender_friends_list, created = FriendList.objects.get_or_create(
            user=self.sender
        )
        sender_friends_list.add_friend(self.receiver)
        self.cancel()

    def decline(self):
        self.cancel()

    def cancel(self):
        self.is_active = False
        self.save()
