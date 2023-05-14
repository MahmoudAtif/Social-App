from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from project.posts.serializers.v1 import PostSerializer, ShareSerializer, PostDetailSerializer
from project.posts.models import Post, Share, Favorite
from project.posts.permissions import UserPostPermission
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination


class PostViewSet(viewsets.ModelViewSet):

    queryset = (
        Post.objects
        .annotate_total_likes()
        .annotate_total_comments()
        .annotate_total_shares()
        .annotate_total_tags()
        .select_related('user')
        .prefetch_related('tags')
        .filter(is_published=True)
    )
    permission_classes = (UserPostPermission,)
    serializer_class = PostSerializer
    filter_backends = [SearchFilter]
    search_fields = ['content', 'user__username', 'user__email']

    def list(self, request, *args, **kwargs):
        friends_ids = request.user.friends.select_related('user').values_list(
            'user__id', flat=True
        )
        friends_ids = list(friends_ids)
        friends_ids.append(request.user.id)

        posts = (
            self.get_queryset()
            .filter(user__id__in=friends_ids, is_published=True)
            .exclude(privacy=Post.PrivacyEnum.PRIVATE)
        )
        shared_posts = (
            Share.objects.filter(user__id__in=friends_ids)
            .select_related('user', 'post', 'post__user')
            .prefetch_related('post__likes', 'post__tags')
        )

        post_serializer = PostSerializer(posts, many=True)
        share_serializer = ShareSerializer(shared_posts, many=True)

        paginator = PageNumberPagination()
        paginated_queryset = paginator.paginate_queryset(
            post_serializer.data + share_serializer.data,
            request
        )
        paginated_response = paginator.get_paginated_response(
            paginated_queryset
        )
        return paginated_response

    def retrieve(self, request, pk, *args, **kwargs):
        post = self.get_object()
        if not post.user == request.user:
            if post.is_private():
                return Response(
                    {
                        'detail': 'Not Found'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            if not post.user.friends_list.is_mutual(request.user) and not post.is_public():
                return Response(
                    {
                        'detail': 'Not Found'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

        serializer = PostDetailSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {
                'request': self.request
            }
        )
        return context

    @action(
        methods=['POST'],
        detail=True
    )
    def like(self, request, pk, *args, **kwargs):
        post = self.get_object()
        post.like(request.user)
        return Response(
            {
                'message': 'Success'
            },
            status=status.HTTP_200_OK
        )

    @action(
        methods=['POST'],
        detail=True
    )
    def unlike(self, request, pk, *args, **kwargs):
        post = self.get_object()
        post.unlike(request.user)
        return Response(
            {
                'message': 'Success'
            },
            status=status.HTTP_200_OK
        )

    @action(
        methods=['POST'],
        detail=True
    )
    def share(self, request, pk, *args, **kwargs):
        post = self.get_object()
        content = request.data.get('content', '')
        Share.objects.create(
            user=request.user,
            post=post,
            content=content
        )
        return Response(
            {
                'message': 'Success'
            },
            status=status.HTTP_200_OK
        )

    @action(
        methods=['POST'],
        detail=True
    )
    def add_to_favorite(self, request, *args, **kwargs):
        post = self.get_object()
        user_favorite, created = Favorite.objects.get_or_create(
            user=request.user
        )
        user_favorite.add_favorite(post)
        return Response(
            {
                'message': 'Success'
            },
            status=status.HTTP_200_OK
        )

    @action(
        methods=['POST'],
        detail=True
    )
    def remove_from_favorite(self, request, *args, **kwargs):
        post = self.get_object()
        user_favorite, created = Favorite.objects.get_or_create(
            user=request.user
        )
        user_favorite.remove_favorite(post)
        return Response(
            {
                'message': 'Success'
            },
            status=status.HTTP_200_OK
        )
