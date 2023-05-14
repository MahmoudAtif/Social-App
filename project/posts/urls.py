from django.urls import path, include
from rest_framework.routers import DefaultRouter
from project.posts.views import v1

router = DefaultRouter()
router.register('posts', v1.PostViewSet)
router.register('comment', v1.CommentViewSet)

urlpatterns = [
    path('', include(router.urls))
]
