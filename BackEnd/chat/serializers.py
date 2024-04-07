from rest_framework import serializers

from user.serializers import UserSerializer
from core.models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):

    sent_by = UserSerializer(read_only=True)
    sent_to = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["id", "body", "sent_by", "sent_to", "created_at_formatted"]


class ConversationSerializer(serializers.ModelSerializer):

    users = UserSerializer(read_only=True, many=True)
    messages = MessageSerializer(read_only=True, many=True)

    class Meta:
        model = Conversation
        fields = ["id", "users", "messages", "modified_at_formatted"]
