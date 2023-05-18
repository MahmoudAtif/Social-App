from rest_framework import serializers
from project.posts.models import Post
from project.users.serializers.v1 import UserDisplay
from django.utils import timezone
from django.utils.timesince import timesince


class PostSerializer(serializers.ModelSerializer):
    user = UserDisplay(read_only=True)
    tags = serializers.ListSerializer(
        child=serializers.StringRelatedField(),
        required=False
    )
    is_liked = serializers.SerializerMethodField('get_liked')
    time_since = serializers.SerializerMethodField('get_time_since')
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

    def get_liked(self, post):
        user = self.context['request'].user
        if user in post.likes.all():
            return True
        return False

    def get_time_since(self, post):
        created_at = post.created_at
        date_now = timezone.now()
        return timesince(created_at, date_now, depth=1)
