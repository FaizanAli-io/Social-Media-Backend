import uuid

from django.db import models

from django.conf import settings

from django.utils import timezone

from django.utils.timesince import timesince

from django.contrib.auth.models import (
    UserManager,
    AbstractBaseUser,
    PermissionsMixin,
)

# Generics


class BaseModel(models.Model):

    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


# User related


class CustomUserManager(UserManager):

    def _create_user(self, name, email, password, **extra_fields):
        if not email:
            raise ValueError("You must provide a valid E-mail address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(name, email, password, **extra_fields)

    def create_superuser(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(name, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):

    # Attributes
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True, null=True, default="")
    avatar = models.ImageField(upload_to="avatars", blank=True, null=True)
    post_count = models.IntegerField(default=0)
    friend_count = models.IntegerField(default=0)
    friends = models.ManyToManyField("self", blank=True)
    people_you_may_know = models.ManyToManyField("self", blank=True)

    # Permissions
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Dates
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def avatar_url(self):
        return (
            settings.WEBSITE_URL + self.avatar.url
            if self.avatar
            else "https://placehold.co/300"
        )


class FriendRequest(BaseModel):

    SENT = "sent"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

    STATUS_CHOICES = (
        (SENT, "Sent"),
        (ACCEPTED, "Accepted"),
        (REJECTED, "Rejected"),
    )

    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Attributes
    created_by = models.ForeignKey(
        User, related_name="created_friend_request", on_delete=models.CASCADE
    )
    created_for = models.ForeignKey(
        User, related_name="received_friend_request", on_delete=models.CASCADE
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=SENT)

    # Dates
    created_at = models.DateTimeField(auto_now_add=True)


# Post related


class Like(BaseModel):

    # Attributes
    created_by = models.ForeignKey(User, related_name="likes", on_delete=models.CASCADE)

    # Dates
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(BaseModel):

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


class PostAttachment(BaseModel):

    # Attributes
    image = models.ImageField(upload_to="post_attachments/")
    created_by = models.ForeignKey(
        User, related_name="post_attachments", on_delete=models.CASCADE
    )

    def image_url(self):
        return settings.WEBSITE_URL + self.image.url if self.image else ""


class Post(BaseModel):

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


class Hashtag(BaseModel):

    # Attributes
    content = models.CharField(max_length=50)
    occurrence = models.IntegerField(default=0)

    # Dates
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.content} - {self.occurrence}"

    class Meta:
        ordering = ["-occurrence"]


# Chat related


class Conversation(BaseModel):

    # Attributes
    users = models.ManyToManyField(User, related_name="conversations")

    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-modified_at"]

    def modified_at_formatted(self):
        return timesince(self.modified_at)


class ConversationMessage(BaseModel):

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


# Notifications


class Notification(BaseModel):

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
        return f"""
        {self.notification_type}: 
        {self.created_by.name} -> 
        {self.created_for.name} 
        {"Read" if self.is_read else "Unread"}
        """
