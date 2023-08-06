import math
from typing import TypeVar, List

from django.db.models import QuerySet
from django.http import HttpRequest, QueryDict
from pursuitlib.parsing import parseint


DEFAULT_PAGE_SIZE = 20
DEFAULT_MAX_PREV = 2
DEFAULT_MAX_NEXT = 2

T = TypeVar("T")


def page_query(request: HttpRequest, query: QuerySet[T],
                     page_var: str = "page", page_size: int = DEFAULT_PAGE_SIZE,
                     max_prev: int = DEFAULT_MAX_PREV, max_next: int = DEFAULT_MAX_NEXT) -> (List[T], dict):
    page = parseint(request.GET.get(page_var), 1)
    total = query.count()
    last_page = math.ceil(total / page_size)
    page = max(1, min(page, last_page))

    data = query[(page - 1) * page_size:page * page_size].all()

    prev_count = min(page - 1, max_prev)
    prev_pages = range(page - prev_count, page)

    next_count = min(last_page - page, max_next)
    next_pages = range(page + 1, page + 1 + next_count)

    url_query = QueryDict(mutable=True)
    for key in request.GET.keys():
        if key == page_var:
            continue
        url_query.setlist(key, request.GET.getlist(key))
    url_query_prefix = f"?{url_query.urlencode()}&" if len(url_query) > 0 else "?"

    return data, {
        "prev": prev_pages,
        "current": page,
        "next": next_pages,
        "last": last_page,
        "url_query_prefix": url_query_prefix,
    }
