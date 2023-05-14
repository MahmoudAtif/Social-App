from project.users.models import SendEmail
from project.users.serializers.v1 import ChangePasswordSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from project.utils.messages import SUCCESS_CHANGE_PASSWORD_MESSAGE, SUCCESS_CHANGE_PASSWORD_SUBJECT


class ChangePasswordView(APIView):

    serializer_class = ChangePasswordSerializer

    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        user = request.user
        new_password = serializer.validated_data['new_password']

        user.set_password(new_password)
        user.save()

        # send sucess change password
        SendEmail.objects.create(
            email_type='REGULAR_EMAIL',
            email=user.email,
            subject=SUCCESS_CHANGE_PASSWORD_SUBJECT,
            message=SUCCESS_CHANGE_PASSWORD_MESSAGE
        )
        return Response(
            {
                'message': 'Password changed Successfully'
            }
        )
