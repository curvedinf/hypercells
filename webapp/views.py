from django.shortcuts import render
from django.core import serializers

from webapp.models import Person

import hypercells


def index(request):

    qs = Person.objects.all().order_by("first_name", "last_name")

    context = hypercells.create(qs,displayed_fields=["first_name","last_name"])
    context2 = hypercells.create(qs,hidden_fields=["first_name","last_name"])

    return render(request, "templates/index.html", {"context": context, "context2": context2})
