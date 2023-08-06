import json

from django.core.exceptions import BadRequest, PermissionDenied
from django.http import HttpRequest, HttpResponse
from pursuitlib.decorators import decorator


@decorator
def api_get(function, public = False):
    def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.method != "GET":
            raise BadRequest(f"Only GET requests are allowed")
        # noinspection PyUnresolvedReferences
        if not public and request.user.is_anonymous:
            raise PermissionDenied()
        return function(request, *args, **kwargs)
    return wrapper


@decorator
def api_post(function, public = False):
    def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.method != "POST":
            raise BadRequest(f"Only POST requests are allowed")
        # noinspection PyUnresolvedReferences
        if not public and request.user.is_anonymous:
            raise PermissionDenied()

        try:
            data = json.loads(request.body)
        except:
            raise BadRequest("Invalid JSON payload")

        return function(request, *args, data=data, **kwargs)
    wrapper.csrf_exempt = True
    return wrapper
