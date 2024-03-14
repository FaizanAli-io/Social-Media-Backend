from rest_framework.serializers import ModelSerializer

from account.serializers import UserSerializer

from .models import Post, Comment, PostAttachment


class PostAttachmentSerializer(ModelSerializer):

    class Meta:
        model = PostAttachment
        fields = ["id", "image_url"]


class CommentSerializer(ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "body", "created_by", "created_at_formatted"]


class PostSerializer(ModelSerializer):
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "body",
            "like_count",
            "comment_count",
            "comments",
            "created_by",
            "created_at_formatted",
            "attachments",
        ]
