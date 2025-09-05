from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.core.admin import BaseAdmin
from ..models import Token


@admin.register(Token)
class TokenAdmin(BaseAdmin):
    """UI for Token model."""

    ordering = ("-issued",)
    readonly_fields = (
        "jti",
        "issued",
        "expires",
        "is_active_display",
    )
    list_display = (
        "user",
        "kind",
        "issued",
        "expires",
        "is_active_display",
        "revoked",
        "ip",
    )
    list_display_links = (
        "user",
        "kind",
    )
    list_filter = (
        "kind",
        "revoked",
        "issued",
        "expires",
    )
    search_fields = (
        "user__username",
        "user__email",
        "jti",
        "ip",
    )
    list_select_related = ("user",)
    date_hierarchy = "issued"

    fieldsets = (
        (
            None, {
                "fields": (
                    "user",
                    "kind",
                    "jti",
                ),
            },
        ),
        (
            _("Timestamps"), {
                "fields": (
                    "issued",
                    "expires",
                    "is_active_display",
                ),
            },
        ),
        (
            _("Status"), {
                "fields": (
                    "revoked",
                ),
            },
        ),
        (
            _("Request info"), {
                "fields": (
                    "user_agent",
                    "ip",
                ),
            },
        ),
    )

    def is_active_display(self, obj) -> str:
        """Return formatted active status."""
        return _("Yes") if obj.is_active() else _("No")

    is_active_display.short_description = _("Is active")
    is_active_display.admin_order_field = "revoked"