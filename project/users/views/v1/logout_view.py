from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token


class LogoutView(APIView):

    def post(self, request):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response(
            {
                'message': 'Logout Successfully'
            },
            status=status.HTTP_204_NO_CONTENT
        )
