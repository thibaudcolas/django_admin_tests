from pathlib import Path
from django.contrib import admin
from django.urls import path, include
from django.views.debug import default_urlconf
from django.http import Http404, HttpResponse
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.views.static import directory_index
from django.views.csrf import csrf_failure
from demo.views import example_form, variant_home
from demo.admin import admin_site


def page_not_found(request):
    request.META = {
        "SERVER_NAME": "Hello",
        "SERVER_PORT": 1337,
    }
    raise Http404("Test 404 view")


def server_error(request):
    request.META = {
        "SERVER_NAME": "Hello",
        "SERVER_PORT": 1337,
    }
    raise TypeError("Test 500 view")


def server_error_template_missing(request):
    request.META = {
        "SERVER_NAME": "Hello",
        "SERVER_PORT": 1337,
    }
    # Render a "foo" template that does not exist to raise a TemplateDoesNotExist:
    return render(request, "foo.html")


def server_error_template_broken(request):
    request.META = {
        "SERVER_NAME": "Hello",
        "SERVER_PORT": 1337,
    }
    return render(request, "demo/broken_template.html")


def server_error_unicode(request):
    request.META = {
        "SERVER_NAME": "Hello",
        "SERVER_PORT": 1337,
    }
    # Raise a UnicodeError
    r = HttpResponse()
    r.headers.__setitem__("føø", "bar")


def server_error_plaintext(request):
    request.META = {
        "SERVER_NAME": "Hello",
        "SERVER_PORT": 1337,
        # Modify the request to not accept text/html
        "HTTP_ACCEPT": "text/plain",
    }
    raise TypeError("Test 500 view")


def permission_denied(request):
    request.META = {
        "SERVER_NAME": "Hello",
        "SERVER_PORT": 1337,
    }
    raise PermissionDenied("Test 403 view")


def bad_request(request):
    request.META = {
        "SERVER_NAME": "Hello",
        "SERVER_PORT": 1337,
    }
    raise SuspiciousOperation("Test 400 view")


def directory(request):
    return directory_index("./", Path.cwd())


urlpatterns = [
    path("", variant_home, name="variant_home"),
    path("forms/example_form/<as_type>/", example_form),
    path("debug/default_urlconf/", default_urlconf),
    # https://docs.djangoproject.com/en/3.0/ref/views/#error-views
    path("defaults/404/", page_not_found),
    path("defaults/500/", server_error),
    path("defaults/500-template-missing/", server_error_template_missing),
    path("defaults/500-template-broken/", server_error_template_broken),
    path("defaults/500-unicode/", server_error_unicode),
    path("defaults/500-plain-text/", server_error_plaintext),
    path("defaults/403/", permission_denied),
    path("defaults/400/", bad_request),
    path("defaults/csrf_failure/", csrf_failure),
    path("defaults/directory_index/", directory),
    path("flatpages/", include("django.contrib.flatpages.urls")),
    path(
        "admin/password_reset/",
        auth_views.PasswordResetView.as_view(),
        name="admin_password_reset",
    ),
    path(
        "admin/password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin_site.urls),
]
