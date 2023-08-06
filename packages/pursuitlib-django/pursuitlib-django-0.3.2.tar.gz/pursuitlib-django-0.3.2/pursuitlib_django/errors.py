from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from pursuitlib_django.api.utils import response_message


# The site-specific error templates are supposed to be present in "error/<error_code>.html"


def handle_error(request: HttpRequest, code: int, name: str) -> HttpResponse:
    # If the request accepts a web page, return a standard human-readable error page
    if request.accepts("text/html"):
        return render(request, f"error/{code}.html", status=code)

    # Default to responding with a JSON error
    return response_message(name, code)


def error_400(request: HttpRequest, exception: Exception) -> HttpResponse:
    return handle_error(request, 400, "Bad request")


def error_403(request: HttpRequest, exception: Exception) -> HttpResponse:
    return handle_error(request, 403, "Forbidden")


def error_404(request: HttpRequest, exception: Exception) -> HttpResponse:
    return handle_error(request, 404, "Not found")


def error_500(request: HttpRequest) -> HttpResponse:
    return handle_error(request, 500, "Internal server error")
