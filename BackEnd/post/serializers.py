from account.serializers import UserSerializer

from rest_framework.serializers import ModelSerializer

from core.models import Post, Comment, PostAttachment, Hashtag


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
            "is_private",
            "attachments",
            "like_count",
            "comments",
            "comment_count",
            "created_by",
            "created_at_formatted",
        ]


class HashtagSerializer(ModelSerializer):

    class Meta:
        model = Hashtag
        fields = ["id", "content", "occurrence", "modified_at"]
