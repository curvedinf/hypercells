from django.shortcuts import render
from django.core import serializers

from webapp.models import Person

import hypercells


def index(request):

    qs = Person.objects.all().order_by("first_name")

    uid = "index"

    context = hypercells.create(uid, qs)

    return render(request, "templates/index.html", {"context": context})
