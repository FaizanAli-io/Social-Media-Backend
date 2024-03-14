from rest_framework import serializers

from .models import (
    User,
    FriendRequest,
)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "name", "email", "post_count", "friend_count", "avatar_url"]


class FriendRequestSerializer(serializers.ModelSerializer):

    created_by = UserSerializer()

    class Meta:
        model = FriendRequest
        fields = ["id", "created_by"]
