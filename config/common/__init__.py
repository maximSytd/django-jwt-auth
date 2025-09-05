from .authentication import *
from .databases import *
from .installed_apps import *
from .internationalization import *
from .middleware import *
from .paths import *
from .storage import *
from .templates import *
from .drf import *

APPEND_SLASH = False
ALLOWED_HOSTS = ["*"]
SITE_ID = 1
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TESTING = False
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
