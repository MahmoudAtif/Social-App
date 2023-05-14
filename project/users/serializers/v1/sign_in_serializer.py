from rest_framework import serializers
from django.contrib.auth import authenticate


class SignInSerializer(serializers.Serializer):
    email_username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email_username = attrs['email_username']
        password = attrs['password']
        user = authenticate(username=email_username, password=password)

        if user is not None:
            if not user.is_active:
                raise serializers.ValidationError(
                    {
                        'error': 'Your acoount is disable',
                        'status': 'User inactive'
                    }
                )
        else:
            raise serializers.ValidationError(
                {
                    'error': 'unable to login with provided credential',
                }
            )

        attrs['user'] = user
        return attrs
