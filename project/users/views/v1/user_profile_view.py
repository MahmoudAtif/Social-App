from project.posts.serializers.v1 import PostSerializer
from project.posts.models import Post
from project.users.serializers.v1 import UserProfileSerializer
from rest_framework.response import Response
from rest_framework import viewsets, status, mixins
from project.users.models import User
from project.users.permissions import UserPermission
from django.db.models.aggregates import Count
from django.db.models.functions import Coalesce
from rest_framework.decorators import action
from project.friends.serializers.v1 import FriendListSerializer
from project.friends.models import FriendList, FriendRequest
from rest_framework.permissions import IsAuthenticated


class UserProfileViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.RetrieveModelMixin):

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (UserPermission,)

    @action(
        methods=['GET'],
        detail=True
    )
    def friends(self, request, pk, *args, **kwargs):
        user = self.get_object()

        friend_list, created = FriendList.objects.annotate(
            total_friends=Count('friends'),
        ).get_or_create(user=user)

        serializer = FriendListSerializer(instance=friend_list, many=False)
        return Response(
            {
                'message': 'SUCCESS',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

    @action(
        methods=['POST'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def send_friend_request(self, request, *args, **kwargs):
        user = self.get_object()
        friend_request, created = FriendRequest.objects.get_or_create(
            sender=request.user,
            receiver=user,
            is_active=True
        )
        return Response(
            {
                'message': 'SUCCESS',
            },
            status=status.HTTP_200_OK
        )

    @action(
        methods=['POST'],
        detail=True,
        url_path=r"friends/(?P<friend_pk>[^/.]+)/unfriend",
        permission_classes=(UserPermission,)
    )
    def unfriend(self, request, *args, **kwargs):
        user = self.get_object()
        friend_pk = kwargs.get('friend_pk')
        friend = user.friends_list.friends.filter(pk=friend_pk).first()
        if not friend:
            return Response(
                {
                    'message': 'Not friends',
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        user.friends_list.unfriend(friend)
        return Response(
            {
                'message': 'SUCCESS',
            },
            status=status.HTTP_200_OK
        )

    @action(
        methods=['GET'],
        detail=False,
    )
    def posts(self, request, *args, **kwargs):
        posts = Post.objects.filter(user=request.user)

        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = PostSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
