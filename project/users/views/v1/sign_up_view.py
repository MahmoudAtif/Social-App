from rest_framework import generics
from project.users.models import User
from project.users.serializers.v1 import SignUpSerializer


class SignUpView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = ()
