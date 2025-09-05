from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BooksAppConfig(AppConfig):
    """
    Default configuration for Books app.

    This app need to test permissions
    """

    name = "apps.books"
    verbose_name = _("Books")
