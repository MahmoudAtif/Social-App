from rest_framework import serializers
from project.users.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'image'
        )

class UserDisplay(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'image'
        )