"""
Copyright 2023 Djangoist.com 
Distributed publicly under the CC BY-NC-ND 4.0 license
https://creativecommons.org/licenses/by-nc-nd/4.0/
"""

from django.shortcuts import render
from django.core import serializers

from app_example.models import Person

import hypercells.lib


def index(request):
    return render(request, "templates/index.html", {})


def basic(request):
    qs = Person.objects.all()
    context = hypercells.lib.create(qs)
    return render(request, "templates/basic.html", {"context": context})


def multiple(request):
    qs = Person.objects.all().order_by("last_name", "first_name")[:10000]

    context = hypercells.lib.create(
        qs,
        uid=hypercells.lib.create_uid_from_user(request, "first-last"),
        displayed_fields=["first_name", "last_name"],
        field_order=["last_name", "first_name"],
        enforce_security=True,
        request=request,
    )

    qs2 = Person.objects.all().order_by("company_name", "email")[:10000]
    context2 = hypercells.lib.create(
        qs2,
        uid=hypercells.lib.create_uid_from_user(request, "ignore-first-last"),
        hidden_fields=["first_name", "last_name"],
        transmitted_fields=["first_name", "last_name"],
        field_order=["company_name", "email"],
        display_thead=False,
    )

    return render(
        request, "templates/multiple.html", {"context": context, "context2": context2}
    )


def cards(request):
    qs = Person.objects.all().order_by("last_name", "first_name")

    context = hypercells.lib.create(
        qs,
        uid=hypercells.lib.create_uid_from_user(request, "card"),
        transmitted_fields=[
            "first_name",
            "last_name",
            "company_name",
            "address",
            "city",
            "county",
            "state",
            "zip",
            "phone1",
            "phone2",
            "email",
            "web",
        ],
        enforce_security=True,
        request=request,
        display_thead=False,
        templates={hypercells.lib.HC_TEMPLATE_TR_JS: "cards_tr_js.html"},
        css_classes={"table": "table table-responsive table-borderless"},
    )

    return render(request, "templates/cards.html", {"context": context})
