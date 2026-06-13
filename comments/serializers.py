from rest_framework import serializers

from .models import Comment


class RecursiveCommentSerializer(
    serializers.ModelSerializer
):

    replies = serializers.SerializerMethodField()

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    class Meta:

        model = Comment

        fields = [
            "id",
            "ticket",
            "user",
            "username",
            "parent",
            "content",
            "is_deleted",
            "created_at",
            "replies",
        ]

        read_only_fields = [
            "user",
            "is_deleted",
        ]

    def get_replies(self, obj):

        replies = obj.replies.filter(
            is_deleted=False
        )

        serializer = RecursiveCommentSerializer(
            replies,
            many=True
        )

        return serializer.data