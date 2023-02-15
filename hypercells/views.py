"""
Copyright 2023 Djangoist.com 
Distributed publicly under the CC BY-NC-ND 4.0 license
https://creativecommons.org/licenses/by-nc-nd/4.0/
"""

import json
from datetime import datetime

from django.http import HttpResponse
from django.core.exceptions import BadRequest
from hypercells import lib


def get(request):
    if "uid" not in request.GET:
        raise BadRequest('"uid" GET argument is required')
    uid = request.GET["uid"]

    if "page" not in request.GET:
        raise BadRequest('"page" GET argument is required')
    try:
        page = int(request.GET["page"])
    except ValueError:
        raise BadRequest('"page" GET argument must be an integer value')
    if page < 0:
        raise BadRequest('"page" GET argument must not be negative')

    pages = lib.view(uid, page, request)

    class DatetimeEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            return super().default(obj)

    return HttpResponse(
        json.dumps(pages, cls=DatetimeEncoder), content_type="application/json"
    )
