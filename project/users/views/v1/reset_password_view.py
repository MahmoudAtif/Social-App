from rest_framework import status
from rest_framework import generics
from project.users.models import SendEmail
from project.users.serializers.v1 import ResetPasswordSerializer
from rest_framework.response import Response


class ResetPasswordView(generics.CreateAPIView):

    serializer_class = ResetPasswordSerializer
    permission_classes = ()
    throttle_scope = 'reset_password'

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        SendEmail.objects.create(
            email_type='RESET_PASSWORD',
            email=user.email
        )
        return Response(
            {
                'message': 'Check your email for Reset Password'
            },
            status=status.HTTP_200_OK
        )
