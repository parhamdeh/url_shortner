"""
Django Middleware Configuration.

This module defines the middleware stack for the Django project.
Middleware are hooks into Django's request/response processing.
They are executed in the order listed here.

Each middleware component can modify requests and responses,
handle sessions, enforce security, and more.
"""

# ---------------------------------------------------------------------------- #
#                            THIRD PARTY MIDDLEWARES                           #
# ---------------------------------------------------------------------------- #

THIRD_PARTY_MIDDLEWARES = []

# ---------------------------------------------------------------------------- #
#                              DEFAULT MIDDLEWARES                             #
# ---------------------------------------------------------------------------- #

DEFAULT_MIDDLEWARES = [
    # Handles security headers and settings like SECURE_HSTS_SECONDS, SECURE_SSL_REDIRECT
    "django.middleware.security.SecurityMiddleware",
    # Enables internationalization; activates language based on request session or headers
    "django.middleware.locale.LocaleMiddleware",
]

# ---------------------------------------------------------------------------- #
#                               LOCAL MIDDLEWARES                              #
# ---------------------------------------------------------------------------- #

LOCAL_MIDDLEWARES = []

MIDDLEWARE = THIRD_PARTY_MIDDLEWARES + DEFAULT_MIDDLEWARES + LOCAL_MIDDLEWARES
