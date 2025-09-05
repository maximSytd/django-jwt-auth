from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from imagekit.admin import AdminThumbnail

from apps.core.admin import BaseAdmin

from ..models import User


@admin.register(User)
class UserAdmin(BaseAdmin, DjangoUserAdmin):
    """UI for User model."""

    ordering = ("email",)
    avatar_thumbnail = AdminThumbnail(image_field="avatar_thumbnail")
    readonly_fields = (
        "last_login",
    )
    list_display = (
        "avatar_thumbnail",
        "email",
        "username",
        "is_superuser",
        "last_login",
    )
    list_display_links = (
        "username",
        "email",
    )
    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
    )
    add_fieldsets = (
        (
            None, {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    fieldsets = (
        (
            None, {
                "fields": (
                    "username",
                    "email",
                    "password",
                ),
            },
        ),
        (
            _("Personal info"), {
                "fields": (
                    "first_name",
                    "last_name",
                    "avatar",
                    "last_login",
                ),
            },
        ),
        (
            _("Permissions"), {
                "fields": (
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )