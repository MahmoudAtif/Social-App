import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from project.users.models import User


class GuestSignUpView(APIView):

    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        user = User.objects.create_user(
            username='guest' + str(random.randint(0, 99999990)),
            email='guest' + str(random.randint(0, 99999990)) + '@example.com',
            is_guest=True,
        )
        return Response(
            {
                'message': 'SUCCESS',
                'token': user.get_token()
            },
            status=status.HTTP_200_OK
        )
