"""
Security Settings Module.

This module contains settings for security in the Django application.
"""

from config.settings.env import env

SECRET_KEY = env.str("SECRET_KEY")
DEBUG = env.bool("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
