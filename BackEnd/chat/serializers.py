from rest_framework import serializers

from account.serializers import UserSerializer

from core.models import Conversation, ConversationMessage


class ConversationSerializer(serializers.ModelSerializer):

    users = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Conversation
        fields = ["id", "users", "modified_at_formatted"]


class ConversationMessageSerializer(serializers.ModelSerializer):

    sent_by = UserSerializer(read_only=True)
    sent_to = UserSerializer(read_only=True)

    class Meta:
        model = ConversationMessage
        fields = ["id", "body", "sent_by", "sent_to", "created_at_formatted"]


class ConversationDetailSerializer(serializers.ModelSerializer):

    messages = ConversationMessageSerializer(read_only=True, many=True)

    class Meta:
        model = Conversation
        fields = ["id", "users", "messages", "modified_at_formatted"]
