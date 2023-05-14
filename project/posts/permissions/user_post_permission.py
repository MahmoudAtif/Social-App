from rest_framework.permissions import IsAuthenticated, SAFE_METHODS


class UserPostPermission(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user == obj.user
        )
