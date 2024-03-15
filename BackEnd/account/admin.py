from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from . import models


class CustomUserAdmin(UserAdmin):
    ordering = ["email"]
    list_display = ["email", "name"]

    fieldsets = (
        (_("Credentials"), {"fields": ("email", "password")}),
        (_("Personal Info"), {"fields": ("name", "avatar")}),
        (
            _("Social Information"),
            {
                "fields": (
                    "friends",
                    "post_count",
                    "friend_count",
                    "people_you_may_know",
                )
            },
        ),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser")}),
        (_("Important Dates"), {"fields": ("date_joined", "last_login")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("name", "email", "password1", "password2"),
            },
        ),
    )

    readonly_fields = ["date_joined", "last_login"]


admin.site.register(models.User, CustomUserAdmin)
admin.site.register(models.FriendRequest)
