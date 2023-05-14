from rest_framework import serializers
from project.posts.models import Share
from . import PostSerializer
from project.posts.models import Post


class ShareSerializer(serializers.ModelSerializer):
    post = PostSerializer()

    class Meta:
        model = Share
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['model'] = 'share'
        return representation
