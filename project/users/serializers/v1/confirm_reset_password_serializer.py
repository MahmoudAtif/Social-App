
from rest_framework import serializers


class ConfirmResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        new_password = attrs['new_password']
        confirm_password = attrs['confirm_password']

        if new_password and confirm_password and new_password != confirm_password:
            raise serializers.ValidationError({
                "error": "password didn't match!!"
            })
        return attrs
