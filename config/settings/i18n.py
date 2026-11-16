"""
Internationalization (i18n) & Localization (l10n) Settings

This module configures language and time zone behavior for the Django application.
It ensures that the app supports translations, local date/time formatting,
and proper timezone handling based on Django's built-in i18n/l10n features.
"""

import os

from config.settings.base import BASE_DIR
from config.settings.env import env

LOCALE_PATHS = [os.path.join(BASE_DIR, "app/locale")]

LANGUAGE_CODE = env.str("LANGUAGE_CODE")
LANGUAGES = [("en", "English"), ("fa", "Persian")]

TIME_ZONE = env.str("TIME_ZONE")
USE_I18N = True
USE_TZ = True
