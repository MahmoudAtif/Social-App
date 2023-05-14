from rest_framework import serializers
from project.friends.models import FriendRequest
from project.users.serializers.v1 import UserProfileSerializer


class FriendRequestSerializer(serializers.ModelSerializer):
    sender = UserProfileSerializer()

    class Meta:
        model = FriendRequest
        exclude = ['receiver']
