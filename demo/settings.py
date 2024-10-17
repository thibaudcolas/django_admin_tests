import os
from pathlib import Path

from django.utils.version import get_version

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-!6gle@=ak78)a3oluuqss-1#(e0xwz2wk*f7kkt=vanw#zhhfy"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

# Application definition

INSTALLED_APPS = [
    "demo",
    "debug_toolbar",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.redirects",
    "django.contrib.sites",
    "django.contrib.admindocs",
    "django.contrib.flatpages",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "demo.middleware.AutoLoginMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "demo.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "demo.wsgi.application"


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

if os.environ.get("DATABASE_URL"):
    import dj_database_url

    DATABASES = {"default": dj_database_url.config()}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/dev/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# This is where Django will put files collected from application directories
# and custom directories set in "STATICFILES_DIRS" when
# using "django-admin collectstatic" command.
# https://docs.djangoproject.com/en/stable/ref/settings/#static-root
STATIC_ROOT = BASE_DIR / "static"

#########################################
# Custom settings

# Required for automated tests.
SESSION_COOKIE_HTTPONLY = False

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SITE_ID = 1

VERSION_NUMBERS = {
    "latest": f"v{get_version()}",
    "v5.2": "v5.2",
    "v5.1": "v5.1",
    "v5.0": "v5.0",
    "v4.2": "v4.2",
    "v4.1": "v4.1",
    "v4.0": "v4.0",
    "v3.2": "v3.2",
    "v3.1": "v3.1",
    "v3.0": "v3.0",
    "v2.2": "v2.2",
}

VARIANTS = [
    "English",
    "German",
    "Arabic",
]

LANGUAGE_CODE = os.environ.get("LANGUAGE_CODE", "en-us")
VERSION_NUMBER = os.environ.get("VERSION_NUMBER", list(VERSION_NUMBERS.keys())[0])
VARIANT = os.environ.get("VARIANT", VARIANTS[0])

DATA_UPLOAD_MAX_NUMBER_FIELDS = 1200

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: "admin/" not in request.path,
}


STATIC_URL = f"django_admin_tests/{VERSION_NUMBER}/{VARIANT.lower()}/static/"
