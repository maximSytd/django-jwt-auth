from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Token(BaseModel):
    """Represent authentication token in db."""

    class Kind(models.TextChoices):
        """String enum for token kind choices."""

        ACCESS = "access", _("Access")
        REFRESH = "refresh", _("Refresh")

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="tokens",
    )
    kind = models.CharField(
        max_length=10,
        choices=Kind.choices,
        verbose_name=_("Kind"),
    )
    jti = models.CharField(
        max_length=36,
        verbose_name=_("JTI"),
        help_text=_("JWT token uniqueness identifier preventing recurrence"),
        unique=True,
    )
    issued = models.DateTimeField(
        verbose_name=_("Issued"),
    )
    expires = models.DateTimeField(
        verbose_name=_("Expires"),
    )
    revoked = models.BooleanField(
        default=False,
        verbose_name=_("Revoked"),
    )
    user_agent = models.CharField(
        max_length=512,
        null=True,
        blank=True,
        verbose_name=_("User agent"),
    )
    ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=("IP"),
    )

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "user",
                    "kind",
                    "revoked",
                ],
            ),
            models.Index(
                fields=[
                    "expires",
                ],
            ),
            models.Index(
                fields=[
                    "jti",
                ],
            ),
        ]
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def is_active(self) -> bool:
        """Return boolean of is the token active."""
        return not self.revoked and self.expires > timezone.now()
