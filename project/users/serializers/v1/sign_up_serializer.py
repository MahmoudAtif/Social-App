from rest_framework import serializers
from project.users.models import User
from django.db import transaction


class SignUpSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            'confirm_password',
            'first_name',
            'last_name',
        )
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'first_name': {
                'required': False,
                # 'read_only': True
            },
            'last_name': {
                'required': False,
                # 'read_only': True
            },
        }

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.deactivate()
        return user

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.pop('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError({
                "error": "password didn't match !!"
            })

        return super().validate(attrs)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['message'] = 'Check your Email for Verification'
        representation['token'] = instance.get_token()
        return representation
