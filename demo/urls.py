from django.urls import path, include
from django.shortcuts import redirect, render
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.views.debug import default_urlconf
from django.contrib.auth import views as auth_views


def root(request):
    return redirect(to="home")


def home(request):
    return render(
        request,
        "demo/home.html",
        {
            "version_numbers": settings.VERSION_NUMBERS,
            "variants": settings.VARIANTS,
        },
    )


def version_home(request):
    return redirect(to="variant_home")


urlpatterns = [
    path("", root, name="root"),
    path("django_admin_tests/", home, name="home"),
    path(
        f"django_admin_tests/{settings.VERSION_NUMBER}/",
        version_home,
        name="version_home",
    ),
    path(
        f"django_admin_tests/{settings.VERSION_NUMBER}/{settings.VARIANT.lower()}/",
        include("demo.demo_urls"),
    ),
    path("debug_toolbar/", include("debug_toolbar.urls")),
]

# urlpatterns += i18n_patterns(
#     path(
#         "admin/password_reset/",
#         auth_views.PasswordResetView.as_view(),
#         name="admin_password_reset",
#     ),
#     path(
#         "admin/password_reset/done/",
#         auth_views.PasswordResetDoneView.as_view(),
#         name="password_reset_done",
#     ),
#     path(
#         "reset/<uidb64>/<token>/",
#         auth_views.PasswordResetConfirmView.as_view(),
#         name="password_reset_confirm",
#     ),
#     path(
#         "reset/done/",
#         auth_views.PasswordResetCompleteView.as_view(),
#         name="password_reset_complete",
#     ),
#     path("admin/doc/", include("django.contrib.admindocs.urls")),
#     path("admin/", admin.site.urls),
#     path("congrats/", default_urlconf, name="congrats"),
# )
