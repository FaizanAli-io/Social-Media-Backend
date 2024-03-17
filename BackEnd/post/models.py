import uuid

from django.db import models

from django.conf import settings

from django.utils.timesince import timesince

from account.models import User


class Like(models.Model):

    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Attributes
    created_by = models.ForeignKey(User, related_name="likes", on_delete=models.CASCADE)

    # Dates
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):

    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Attributes
    body = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        User, related_name="comments", on_delete=models.CASCADE
    )

    # Dates
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def created_at_formatted(self):
        return timesince(self.created_at)


class PostAttachment(models.Model):

    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Attributes
    image = models.ImageField(upload_to="post_attachments/")
    created_by = models.ForeignKey(
        User, related_name="post_attachments", on_delete=models.CASCADE
    )

    def image_url(self):
        return settings.WEBSITE_URL + self.image.url if self.image else ""


class Post(models.Model):

    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Attributes
    body = models.TextField(blank=True, null=True)
    is_private = models.BooleanField(default=False)
    reported_by = models.ManyToManyField(User, blank=True)
    attachments = models.ManyToManyField(PostAttachment, blank=True)
    created_by = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)

    # Dates
    created_at = models.DateTimeField(auto_now_add=True)

    # Likes and Comments
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    likes = models.ManyToManyField(Like, blank=True)
    comments = models.ManyToManyField(Comment, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def created_at_formatted(self):
        return timesince(self.created_at)
