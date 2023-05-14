from rest_framework import serializers
from project.users.models import User
from rest_framework.exceptions import NotFound


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField()

    def validate(self, attrs):
        email = attrs['email']
        user = User.objects.filter(email=email).first()

        if user is None:
            raise NotFound({
                'error': 'No account was found with this email'
            })

        attrs['user'] = user
        return attrs
