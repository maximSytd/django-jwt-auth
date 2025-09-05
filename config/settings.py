import decouple

from .common import *

SECRET_KEY = decouple.config("DJANGO_SECRET")

DEBUG = decouple.config("DEBUG", cast=bool)

INTERNAL_IPS = [
    "127.0.0.1",
]

APP_LABEL = "money flow"
