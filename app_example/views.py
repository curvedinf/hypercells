from django.shortcuts import render
from django.core import serializers

from app_example.models import Person

import hypercells.lib


def index(request):

    qs = Person.objects.all().order_by("first_name", "last_name")[:10000]

    context = hypercells.lib.create(qs, displayed_fields=["first_name", "last_name"])
    context2 = hypercells.lib.create(qs, hidden_fields=["first_name", "last_name"])

    return render(
        request, "templates/index.html", {"context": context, "context2": context2}
    )
