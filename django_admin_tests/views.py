from django.shortcuts import render

from .forms import ExampleForm


def example_form(request, as_type="p"):
    if request.method == "POST":
        form = ExampleForm(request.POST)
        form.add_error(None, "An example non-field error.")
    else:
        form = ExampleForm()

    return render(
        request,
        "django_admin_tests/example_form.html",
        {"form": form, "as_type": as_type},
    )
