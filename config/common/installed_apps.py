# Application definition
INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
)

DRF_PACKAGES = (
    "rest_framework",
    "django_filters",
    "drf_spectacular",
    "drf_standardized_errors",
)

THIRD_PARTY = (
    "imagekit",
    "django_extensions",
    "debug_toolbar",
)

LOCAL_APPS = (
    "apps.core",
    "apps.users",
    "apps.books",
)

INSTALLED_APPS += THIRD_PARTY + LOCAL_APPS + DRF_PACKAGES