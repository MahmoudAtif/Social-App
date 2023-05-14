from rest_framework import status
from project.friends.serializers.v1 import FriendRequestSerializer
from rest_framework.response import Response
from project.friends.models import FriendRequest
from rest_framework import mixins, viewsets
from rest_framework.decorators import action


class FriendRequestView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):

    queryset = FriendRequest.objects.filter(is_active=True)
    serializer_class = FriendRequestSerializer

    def list(self, request, *args, **kwargs):
        queryset = FriendRequest.objects.filter(
            receiver=request.user,
            is_active=True
        )
        total_requests = FriendRequest.objects.filter(
            receiver=request.user,
            is_active=True
        ).count()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                'message': 'SUCCESS',
                'data': {
                    'requests': serializer.data,
                    'total_requests': total_requests
                }
            },
            status=status.HTTP_200_OK
        )

    @action(
        methods=['POST'],
        detail=True
    )
    def accept(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response(
                {
                    'error': 'Not Found',
                },
                status=status.HTTP_404_NOT_FOUND
            )
        instance.accept()
        return Response(
            {
                'message': 'SUCCESS',
            },
            status=status.HTTP_200_OK
        )

    @action(
        methods=['POST'],
        detail=True
    )
    def cancel(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response(
                {
                    'error': 'Not Found',
                },
                status=status.HTTP_404_NOT_FOUND
            )
        instance.cancel()
        return Response(
            {
                'message': 'SUCCESS',
            },
            status=status.HTTP_200_OK
        )
