from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from . import models


class CustomUserAdmin(UserAdmin):
    ordering = ["email"]
    list_display = ["email", "name"]

    fieldsets = (
        (
            _("Credentials"),
            {
                "fields": (
                    "id",
                    "email",
                    "password",
                )
            },
        ),
        (
            _("Personal Information"),
            {
                "fields": (
                    "name",
                    "avatar",
                )
            },
        ),
        (
            _("Social Information"),
            {
                "fields": (
                    "post_count",
                    "friend_count",
                    "friends",
                    "people_you_may_know",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (
            _("Important Dates"),
            {
                "fields": (
                    "created_at",
                    "last_login",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "name",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    readonly_fields = ["id", "created_at", "last_login"]


# User related
admin.site.register(models.User, CustomUserAdmin)
admin.site.register(models.FriendRequest)

# Post related
admin.site.register(models.Post)
admin.site.register(models.Like)
admin.site.register(models.Comment)
admin.site.register(models.PostAttachment)
admin.site.register(models.Hashtag)

# Chat related
admin.site.register(models.Conversation)
admin.site.register(models.Message)

# Notifications
admin.site.register(models.Notification)
