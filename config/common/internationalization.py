import os

from .paths import BASE_DIR

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = "Europe/Moscow"

USE_I18N = True
USE_L10N = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)
