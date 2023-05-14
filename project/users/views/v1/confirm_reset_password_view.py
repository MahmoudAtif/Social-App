from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from project.users.models import User, SecretToken, SendEmail
from project.users.serializers.v1 import ConfirmResetPasswordSerializer
from rest_framework.exceptions import ValidationError, NotFound
from project.utils.messages import SUCCESS_RESET_PASSWORD_SUBJECT, SUCCESS_RESET_PASSWORD_MESSAGE


class ConfirmResetPasswordView(generics.CreateAPIView):

    serializer_class = ConfirmResetPasswordSerializer

    def get_token(self):
        key = self.request.GET.get('token', '')
        token = SecretToken.objects.filter(key=key).first()

        if token is None:
            raise NotFound({
                'error': 'token is invalid'
            })

        if token.is_expired:
            raise ValidationError({
                'error': 'token is expired'
            })
        return token

    def get_user(self):
        token = self.get_token()
        user = User.objects.filter(id=token.user.id).first()
        return user

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = self.get_token()
        user = self.get_user()
        new_password = serializer.validated_data['new_password']

        user.set_password(new_password)
        user.save()
        token.deactivate()

        # send sucess reset password
        SendEmail.objects.create(
            email_type='REGULAR_EMAIL',
            email=user.email,
            subject=SUCCESS_RESET_PASSWORD_SUBJECT,
            message=SUCCESS_RESET_PASSWORD_MESSAGE
        )
        return Response(
            {
                'message': 'Password is reset successfully'
            },
            status=status.HTTP_200_OK
        )
