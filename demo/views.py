from django.shortcuts import redirect, render
from django.conf import settings

from .forms import ExampleForm


def variant_home(request):
    return render(
        request,
        "demo/variant_home.html",
        {
            "version_number": settings.VERSION_NUMBER,
            "version_label": settings.VERSION_NUMBERS[settings.VERSION_NUMBER],
            "variant": settings.VARIANT,
        },
    )


def example_form(request, as_type="div"):
    if request.method == "POST":
        form = ExampleForm(request.POST)
        form.add_error(None, "An example non-field error.")
    else:
        form = ExampleForm()

    return render(
        request,
        "demo/example_form.html",
        {"form": form, "as_type": as_type},
    )


def redirect_to_admin(request):
    return redirect("admin:index")
