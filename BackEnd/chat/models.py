from django.db import models

from account.models import User


class Conversation:
    users = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
