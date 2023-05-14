from rest_framework import status
from project.users.serializers.v1 import SignInSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema


class SignInView(APIView):

    serializer_class = SignInSerializer
    permission_classes = ()
    throttle_scope = 'login'

    @swagger_auto_schema(request_body=SignInSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token = user.get_token()

        return Response(
            {
                'token': token,
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            status=status.HTTP_200_OK
        )
