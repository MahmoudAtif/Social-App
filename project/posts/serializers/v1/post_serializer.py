from rest_framework import serializers
from project.posts.models import Post
from project.users.serializers.v1 import UserDisplay


class PostSerializer(serializers.ModelSerializer):
    user = UserDisplay(read_only=True)
    tags = serializers.ListSerializer(
        child=serializers.StringRelatedField(),
        required=False
    )
    total_likes = serializers.IntegerField(read_only=True)
    total_tags = serializers.IntegerField(read_only=True)
    total_comments = serializers.IntegerField(read_only=True)
    total_shares = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        exclude = ['likes']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['model'] = 'post'
        representation['privacy'] = Post.PrivacyEnum(instance.privacy).label
        return representation
