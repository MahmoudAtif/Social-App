from rest_framework import serializers
from project.posts.models import Post
from project.users.serializers.v1 import UserDisplay
from .comment_serializer import CommentSerializer


class PostDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    likes = UserDisplay(many=True, read_only=True)
    tags = serializers.ListSerializer(
        child=serializers.StringRelatedField(),
        required=False
    )
    comments = CommentSerializer(read_only=True, many=True)
    is_liked = serializers.SerializerMethodField('get_liked')
    total_likes = serializers.IntegerField(read_only=True)
    total_tags = serializers.IntegerField(read_only=True)
    total_comments = serializers.IntegerField(read_only=True)
    total_shares = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['model'] = 'post'
        representation['privacy'] = Post.PrivacyEnum(instance.privacy).label
        return representation

    def get_liked(self, post):
        user = self.context['request'].user
        if user in post.likes.all():
            return True
        return False
