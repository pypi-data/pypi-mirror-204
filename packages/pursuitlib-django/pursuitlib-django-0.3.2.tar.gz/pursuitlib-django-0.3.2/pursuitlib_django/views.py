from typing import Type

from django.http import FileResponse
from django.utils.http import content_disposition_header

from pursuitlib_django.forms import Form


def view_form(form_type: Type[Form]):
    return lambda request, **kwargs: form_type.handle_request(request, **kwargs)


def serve_text(text: str, content_type: str = "text/plain", name: str = None) -> FileResponse:
    # When a text content type is used, the text needs to be passed as is.
    # It will then be UTF8-encoded
    return serve_file(text, f"{content_type}; charset=utf-8", name)


def serve_file(content, content_type: str = "application/octet-stream", name: str = None) -> FileResponse:
    resp = FileResponse(content, content_type=content_type, as_attachment=(name is not None), filename=name)
    # Django bugfix: set the Content-Disposition header manually
    resp.headers["Content-Disposition"] = content_disposition_header(resp.as_attachment, resp.filename)
    return resp
