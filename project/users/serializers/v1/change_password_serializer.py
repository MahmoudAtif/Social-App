from rest_framework import serializers


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate_old_password(self, value):
        user = self.context.get('request', None).user

        if not user.check_password(value):
            raise serializers.ValidationError('password is wrong')

        return value
