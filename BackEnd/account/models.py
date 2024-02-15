import uuid

from django.db import models

from django.utils import timezone

from django.contrib.auth.models import (
    UserManager,
    AbstractBaseUser,
    PermissionsMixin,
)


class CustomUserManager(UserManager):

    def _create_user(self, name, email, password, **extra_fields):
        if not email:
            raise ValueError('You must provide a valid E-mail address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, email, password, **extra_fields)

    def create_superuser(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(name, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Attributes
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True, null=True, default='')
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
    post_count = models.IntegerField(default=0)
    friend_count = models.IntegerField(default=0)
    friends = models.ManyToManyField('self')

    # Permissions
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Dates
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def avatar_url(self):
        return "http://127.0.0.1:8000" + self.avatar.url \
            if self.avatar else ''


class FriendRequest(models.Model):

    SENT = 'sent'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    STATUS_CHOICES = (
        (SENT, 'Sent'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    )

    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Attributes
    created_by = models.ForeignKey(User, related_name='created_friend_request',
                                   on_delete=models.CASCADE)
    created_for = models.ForeignKey(User, related_name='received_friend_request',
                                    on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default=SENT)

    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
