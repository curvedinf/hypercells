import json

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

    pages = lib.view(uid, page)

    return HttpResponse(json.dumps(pages), content_type="application/json")
