from django.shortcuts import render
from django.core import serializers

from app_example.models import Person

import hypercells.lib


def index(request):

    qs = Person.objects.all().order_by("first_name", "last_name")[:10000]

    context = hypercells.lib.create(
        qs,
        uid=hypercells.lib.create_uid_from_user(request, 'first-last'),
        displayed_fields=["first_name", "last_name"]
    )
    context2 = hypercells.lib.create(
        qs, 
        uid=hypercells.lib.create_uid_from_user(request, 'other'),
        hidden_fields=["first_name", "last_name"], 
        display_thead=False
    )

    return render(
        request, "templates/index.html", {"context": context, "context2": context2}
    )
