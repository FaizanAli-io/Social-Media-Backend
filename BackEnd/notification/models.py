import uuid

from django.db import models

from post.models import Post
from account.models import User


class Notification(models.Model):

    SENTREQUEST = "sentrequest"
    ACCEPTEDREQUEST = "acceptedrequest"
    REJECTEDREQUEST = "rejectedrequest"
    POSTCOMMENT = "postcomment"
    POSTLIKE = "postlike"

    NOTIFICATION_TYPES = (
        (SENTREQUEST, "Sent Request"),
        (ACCEPTEDREQUEST, "Accepted Request"),
        (REJECTEDREQUEST, "Rejected Request"),
        (POSTCOMMENT, "Post Comment"),
        (POSTLIKE, "Post Like"),
    )

    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Attributes
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)

    # Linkages
    post = models.ForeignKey(Post, blank=True, null=True, on_delete=models.CASCADE)

    created_by = models.ForeignKey(
        User, related_name="created_notifications", on_delete=models.CASCADE
    )

    created_for = models.ForeignKey(
        User, related_name="received_notifications", on_delete=models.CASCADE
    )

    # Dates
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.notification_type}: {self.created_by.name} -> {self.created_for.name} (Read: {self.is_read})"
