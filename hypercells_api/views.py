from django.http import HttpResponse
from django.core.exceptions import BadRequest

from hypercells_api import models

import hypercells


def get(request):
    if "uid" not in request.GET:
        raise BadRequest("uid is required")
    uid = request.GET["uid"]

    if "row" not in request.GET:
        raise BadRequest("row is required")
    try:
        row = int(request.GET["row"])
    except:
        raise BadRequest("row must be an integer value")

    returned_qs = hypercells.view(uid, row)

    return HttpResponse("Here")
