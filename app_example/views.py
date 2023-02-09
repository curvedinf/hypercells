from django.shortcuts import render
from django.core import serializers

from app_example.models import Person

import hypercells.lib


def index(request):
    return render(
        request, "templates/index.html", {}
    )

def basic(request):
    qs = Person.objects.all()
    context = hypercells.lib.create(qs)
    return render(
        request, "templates/basic.html", {"context": context}
    )

def multiple(request):
    qs = Person.objects.all().order_by("first_name", "last_name")[:10000]

    context = hypercells.lib.create(
        qs,
        uid=hypercells.lib.create_uid_from_user(request, "first-last"),
        displayed_fields=["first_name", "last_name"],
        enforce_security=True,
        request=request,
    )
    context2 = hypercells.lib.create(
        qs,
        uid=hypercells.lib.create_uid_from_user(request, "ignore-first-last"),
        hidden_fields=["first_name", "last_name"],
        display_thead=False,
    )

    return render(
        request, "templates/multiple.html", {"context": context, "context2": context2}
    )
