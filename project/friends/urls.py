from django.urls import path, include
from rest_framework.routers import DefaultRouter
from project.friends.views import v1
router = DefaultRouter()
router.register('requests', v1.FriendRequestView, basename='requests')

urlpatterns = [
    path('', include(router.urls))
]
