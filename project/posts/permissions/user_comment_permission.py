from rest_framework.permissions import IsAuthenticated, SAFE_METHODS


class UserCommentPermission(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user == obj.user or
            request.user == obj.post.user
        )
