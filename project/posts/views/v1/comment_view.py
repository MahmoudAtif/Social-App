from rest_framework.exceptions import NotFound
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from project.posts.serializers.v1 import PostSerializer, ShareSerializer, CommentInputSerializer
from project.posts.models import Post, Share, Comment
from project.posts.permissions import UserCommentPermission


class CommentViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentInputSerializer
    permission_classes = (UserCommentPermission,)

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
        comment = Comment.objects.filter(pk=pk).first()
        self.check_comment(comment)
        comment.like(request.user)
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
        comment = Comment.objects.filter(pk=pk).first()
        self.check_comment(comment)
        comment.unlike(request.user)
        return Response(
            {
                'message': 'Success'
            },
            status=status.HTTP_200_OK
        )

    def check_comment(self, comment):
        if not comment:
            raise NotFound(
                {
                    'detail': 'Not Found'
                }
            )
