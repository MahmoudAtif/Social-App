from rest_framework import status
from project.users.models import User, SecretToken, SendEmail
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, NotFound
from project.utils.messages import SUCCESS_ACTIVATION_SUBJECT, SUCCESS_ACTIVATION_MESSAGE


class EmailVerificationView(APIView):

    permission_classes = ()

    def get_token(self):
        key = self.request.GET.get('token')
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

        if user.is_active:
            raise ValidationError({
                'message': 'your account is already activated'
            })
        return user

    def get(self, request):
        token = self.get_token()
        user = self.get_user()

        user.activate()
        token.deactivate()

        # send sucess verification email
        SendEmail.objects.create(
            email_type='REGULAR_EMAIL',
            email=user.email,
            subject=SUCCESS_ACTIVATION_SUBJECT,
            message=SUCCESS_ACTIVATION_MESSAGE
        )
        return Response(
            {
                'message': 'You are active now'
            },
            status=status.HTTP_200_OK
        )
