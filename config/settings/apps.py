"""
Django Applications Module.

In this module, all applications used within the application level are defined. These modules are defined in the
following three categories:

1.Third-party modules installed outside the application
2.The framework's default modules
3.Local modules developed by ourselves

All modules listed in the above categories are stored in the INSTALLED_APPS variable.
"""

# ---------------------------------------------------------------------------- #
#                               THIRD PARTY APPS                               #
# ---------------------------------------------------------------------------- #

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    "drf_spectacular",
    "django_celery_results",
    
]

# ---------------------------------------------------------------------------- #
#                                 DEFAULT APPS                                 #
# ---------------------------------------------------------------------------- #

DEFAULT_APPS = [
    "django.contrib.auth",  # Authentication framework
    "django.contrib.contenttypes",  # Content type system (generic relations)
    "django.contrib.staticfiles",  # Manages static files (CSS, JavaScript, images) in development and production
]

# ---------------------------------------------------------------------------- #
#                                  LOCAL APPS                                  #
# ---------------------------------------------------------------------------- #

LOCAL_APPS = [
    'app.apis',
    'app.users',
    # 'app.shortner',
    # 'app.sms_gatewy',
    # 'app.notification',
    'app.auth',
]

INSTALLED_APPS = THIRD_PARTY_APPS + DEFAULT_APPS + LOCAL_APPS
