"""django_admin_tests URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.debug import default_urlconf
from django.http import Http404
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.contrib.auth import views as auth_views

from .views import example_form


def page_not_found(request):
    raise Http404("Test 404 view")


def server_error(request):
    raise TypeError("Test 500 view")


def permission_denied(request):
    raise PermissionDenied("Test 403 view")


def bad_request(request):
    raise SuspiciousOperation("Test 400 view")


urlpatterns = [
    path("forms/example_form/<as_type>/", example_form),
    path("debug/default_urlconf/", default_urlconf),
    # https://docs.djangoproject.com/en/3.0/ref/views/#error-views
    path("defaults/404/", page_not_found),
    path("defaults/500/", server_error),
    path("defaults/403/", permission_denied),
    path("defaults/400/", bad_request),
    path("pages/", include("django.contrib.flatpages.urls")),
    path("admin/doc/", include("django.contrib.admindocs.urls")),
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
    path("admin/", admin.site.urls),
]
