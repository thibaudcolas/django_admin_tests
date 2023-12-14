from pathlib import Path
from django.contrib import admin
from django.urls import path, include
from django.views.debug import default_urlconf
from django.http import Http404
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.contrib.auth import views as auth_views
from django.views.static import directory_index
from django.views.csrf import csrf_failure
from demo.views import example_form, variant_home

def page_not_found(request):
    raise Http404("Test 404 view")


def server_error(request):
    raise TypeError("Test 500 view")


def permission_denied(request):
    raise PermissionDenied("Test 403 view")


def bad_request(request):
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
    path("admin/docs/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
]
