from rest_framework import status
from project.users.serializers.v1 import ResendEmailVerificationSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema


class ResendEmailVerificationView(APIView):

    serializer_class = ResendEmailVerificationSerializer
    permission_classes = ()
    throttle_scope = 'resend_verification'

    @swagger_auto_schema(request_body=ResendEmailVerificationSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'message': 'Check your email'
            },
            status=status.HTTP_200_OK
        )
