"""Browser-local demo settings. The normal development server is unaffected."""

import os
from pathlib import Path

from .settings import *
from .settings import INSTALLED_APPS, MIDDLEWARE

STATE_DIR = Path(os.environ.get("DEMO_WASM_STATE", "/persist"))
SECRET_KEY = "public-browser-local-django-admin-demo"
# Debug pages are deliberately part of this UI test site.
DEBUG = True
INSTALLED_APPS = [app for app in INSTALLED_APPS if app != "debug_toolbar"]
MIDDLEWARE = [
    middleware
    for middleware in MIDDLEWARE
    if middleware
    not in {
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        "demo.middleware.AutoLoginMiddleware",
    }
]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": STATE_DIR / "db.sqlite3",
    }
}
STATIC_ROOT = os.environ.get("DEMO_WASM_STATIC", str(STATE_DIR / "static"))
STATIC_URL = "/django_admin_tests/static/"
MEDIA_ROOT = STATE_DIR / "media"
VERSION_NUMBER = "latest"
VARIANT = "English"
VARIANTS = [VARIANT]
LANGUAGE_CODE = "en-us"
# The worker keeps its own persistent cookie jar. Rendered form tokens continue
# to use Django's normal CSRF validation, with the secret stored in the session.
CSRF_USE_SESSIONS = True
SESSION_COOKIE_PATH = "/django_admin_tests/"
SESSION_COOKIE_HTTPONLY = True
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"
# Public demo credentials; this database is downloaded by every visitor.
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
