from django.contrib.auth import get_user_model
from django.contrib.auth import login

User = get_user_model()


class AutoLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the user we want to log in as, from cookies.
        if username := request.COOKIES.get("auto_login"):
            user = User.objects.get(username=username)

            # Log in the user
            request.user = user
            login(request, user)

        # Get the user we want to log in as, from headers.
        elif username := request.headers.get("X-Auto-Login"):
            user = User.objects.get(username=username)

            # Log in the user
            request.user = user
            login(request, user)

        response = self.get_response(request)
        return response
