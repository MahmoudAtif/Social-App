from rest_framework import serializers
from project.friends.models import FriendList, FriendRequest
from project.users.serializers.v1 import UserProfileSerializer


class FriendListSerializer(serializers.ModelSerializer):
    """Serializer for Friend List"""
    total_friends = serializers.IntegerField()
    friends = UserProfileSerializer(many=True)

    class Meta:
        model = FriendList
        exclude = ['user']
