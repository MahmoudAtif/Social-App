from rest_framework import serializers
from project.posts.models import Comment


class CommentInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['post', 'comment']

    def create(self, validated_data):
        comment = self.Meta.model(
            user=self.context['request'].user,
            **validated_data
        )
        comment.save()
        return comment
