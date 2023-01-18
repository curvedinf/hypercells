from django.shortcuts import render
from django.core import serializers

from webapp.models import Person

import hypercells


def index(request):

    qs = Person.objects.all().order_by("first_name")

    uid = "index"

    context = hypercells.create(uid, qs)

    rows = serializers.serialize("python", hypercells.view(uid, 0))

    return render(request, "templates/index.html", {"rows": rows, "context": context})
