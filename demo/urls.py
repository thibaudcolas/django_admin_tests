from django.urls import path, include
from django.shortcuts import redirect, render
from django.conf import settings


def root(request):
    return redirect(to="home")


def home(request):
    return render(
        request,
        "demo/home.html",
        {
            "version_numbers": settings.VERSION_NUMBERS,
            "variants": settings.VARIANTS,
        }
    )


def version_home(request):
    return redirect(to="variant_home")


def version_latest(request):
    return redirect(f'/django_admin_tests/{settings.VERSION_NUMBER}/{settings.VARIANT.lower()}/')


urlpatterns = [
    path('', root, name="root"),
    path('django_admin_tests/', home, name="home"),
    path(f'django_admin_tests/{settings.VERSION_NUMBER}/', version_home, name="version_home"),
    path(f'django_admin_tests/latest/{settings.VARIANT.lower()}/', version_latest),
    path(f'django_admin_tests/{settings.VERSION_NUMBER}/{settings.VARIANT.lower()}/', include('demo.demo_urls')),
    path("debug_toolbar/", include("debug_toolbar.urls")),
]
