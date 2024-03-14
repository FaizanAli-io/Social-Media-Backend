import uuid

from account.models import User

from django.db import models
from django.utils.timesince import timesince


class Conversation(models.Model):

    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Attributes
    users = models.ManyToManyField(User, related_name="conversations")

    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-modified_at"]

    def modified_at_formatted(self):
        return timesince(self.modified_at)


class ConversationMessage(models.Model):

    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Attributes
    conversation = models.ForeignKey(
        Conversation, related_name="messages", on_delete=models.CASCADE
    )
    sent_by = models.ForeignKey(
        User, related_name="sent_messages", on_delete=models.CASCADE
    )
    sent_to = models.ForeignKey(
        User, related_name="received_messages", on_delete=models.CASCADE
    )
    body = models.TextField()

    # Dates
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def created_at_formatted(self):
        return timesince(self.created_at)
