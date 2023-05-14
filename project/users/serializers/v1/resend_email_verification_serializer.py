from rest_framework import serializers
from django.contrib.auth import authenticate
from project.users.models import SendEmail


class ResendEmailVerificationSerializer(serializers.Serializer):

    email_username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email_username = attrs['email_username']
        password = attrs['password']
        user = authenticate(username=email_username, password=password)

        if user is None:
            raise serializers.ValidationError(
                {
                    'error': 'unable to access with provided credential'
                }
            )

        if user.is_active:
            raise serializers.ValidationError(
                {
                    'error': 'this account is already activated'
                }
            )

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data.get('user')
        obj = SendEmail.objects.create(
            email_type='EMAIL_VERIFICATION',
            email=user.email
        )
        return obj
