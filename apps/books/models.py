from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Book(BaseModel):
    """Represent Book model in db for permissions test."""

    title = models.CharField(
        max_length=120,
        verbose_name=_("Title"),
    )
    author = models.CharField(
        max_length=120,
        verbose_name=_("Title"),
    )

    class Meta:
        permissions = [
            (
                "can_view_books",
                _("Can view books"),
            ),
        ]
        verbose_name = _("Book")
        verbose_name_plural = _("Books")
