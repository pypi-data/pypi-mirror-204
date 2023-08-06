from typing import Type

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, BadRequest
from django.http import HttpResponse, HttpRequest
from pursuitlib.decorators import decorator
from pursuitlib.parsing import parseas

from pursuitlib_django.forms import Form


# View decorators

def staff_required(function):
    def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        # noinspection PyUnresolvedReferences
        if request.user.is_staff:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied("Only the staff can access this resource")
    return wrapper


def get_form_decorator(base_decorator):
    def form_decorator(function, *dargs, **dkwargs):
        # request needs to be the first argument for compatibility with the view decorator
        def remap_wrapper(request: HttpRequest, form_type: Type[Form], *args, **kwargs) -> HttpResponse:
            return function(form_type, request, *args, **kwargs)

        result = base_decorator(remap_wrapper, *dargs, **dkwargs)

        # Remapping input arguments
        return lambda form_type, request, *args, **kwargs: result(request, form_type, *args, **kwargs)
    return form_decorator


form_login_required = get_form_decorator(login_required)
form_staff_required = get_form_decorator(staff_required)


# Action decorators

@decorator
def action(function, *params, method: str = "POST"):
    def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.method != method:
            raise BadRequest(f"Only {method} requests are allowed here")

        if method == "POST":
            request_data = request.POST
        elif method == "GET":
            request_data = request.GET
        else:
            raise Exception(f"Unsupported HTTP method: {method}")

        data = {}
        for param in params:
            # Cast the parameter in the appropriate type
            if ':' in param:
                parts = param.split(':')
                type_name = parts[0]
                name = parts[1]
            else:
                type_name = "str"
                name = param

            if name not in request_data:
                raise BadRequest(f"Missing '{name}' {method} parameter")
            data[name] = parseas(type_name, request_data[name])
            if data[name] is None:
                raise BadRequest(f"Invalid '{name}' {method} parameter")

        kwargs |= data
        return function(request, *args, **kwargs)

    return wrapper

