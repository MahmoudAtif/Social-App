from rest_framework import serializers
from project.posts.models import Comment
from project.users.serializers.v1 import UserDisplay


class CommentSerializer(serializers.ModelSerializer):
    user = UserDisplay()

    class Meta:
        model = Comment
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['total_likes'] = instance.likes.count()
        return representation
