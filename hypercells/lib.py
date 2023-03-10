"""
Copyright 2023 Djangoist.com 
Distributed publicly under the CC BY-NC-ND 4.0 license
https://creativecommons.org/licenses/by-nc-nd/4.0/
"""

import math
import pickle
import uuid
from datetime import datetime, timedelta
import hmac
import hashlib

from django.urls import path
from django.utils import timezone
from django.forms.models import model_to_dict
from django.core.serializers import serialize
from django.core.exceptions import SuspiciousOperation
from django.conf import settings

from hypercells import models, views

HC_TEMPLATE_JS = "js"
HC_TEMPLATE_TABLE = "table"
HC_TEMPLATE_LOADER = "loader"
HC_TEMPLATE_TD_JS = "td_js"
HC_TEMPLATE_TR_JS = "tr_js"

HC_DEFAULT_TEMPLATES = {
    HC_TEMPLATE_JS: "hypercells_js.html",
    HC_TEMPLATE_TABLE: "hypercells_table.html",
    HC_TEMPLATE_LOADER: "hypercells_loader.html",
    HC_TEMPLATE_TD_JS: "hypercells_td_js.html",
    HC_TEMPLATE_TR_JS: "hypercells_tr_js.html",
}


def get_template_from_context(context, template_name):
    if context is None:
        return HC_DEFAULT_TEMPLATES[template_name]
    template_filename = context.templates.get(template_name, None)
    if template_filename is None or template_filename == "":
        return HC_DEFAULT_TEMPLATES[template_name]
    return template_filename


def create(
    queryset,
    uid=None,
    context_class="",
    display_thead=True,
    num_pages=10,
    page_length=100,
    loading_edge_pages=3,
    displayed_fields=[],
    hidden_fields=[],
    transmitted_fields=[],
    field_order=[],
    css_classes={
        "table": "table table-responsive table-hover",
        "thead": "",
        "thead_tr": "",
        "thead_th": "",
        "tbody": "",
        "tbody_tr": "",
        "tbody_td": "",
    },
    enforce_security=False,
    request=None,
    templates={
        HC_TEMPLATE_JS: None,
        HC_TEMPLATE_TABLE: None,
        HC_TEMPLATE_LOADER: None,
        HC_TEMPLATE_TD_JS: None,
        HC_TEMPLATE_TR_JS: None,
    },
):
    """
    Creates or replaces a hypercells context in the database. A context
    stores the configuration for a hypercells instance, including the
    queryset that will drive it and other options.
    """
    if uid is None:
        uid = uuid.uuid4()

    generated_by = None
    if enforce_security:
        if request is None:
            raise ValueError("If enforce_security is enabled, request must be provided")
        if not request.user.is_anonymous:
            generated_by = request.user

    secret_key = getattr(settings, "SECRET_KEY", "NOTSECURE")
    query_data = pickle.dumps(queryset.query)
    hmac_digest = hmac.new(
        secret_key.encode("utf-8"), query_data, hashlib.sha256
    ).digest()

    context, created = models.Context.objects.update_or_create(
        uid=f"{uid}",
        defaults={
            "model_module": f"{queryset.model.__module__}",
            "model_class": f"{queryset.model.__qualname__}",
            "context_class": context_class,
            "query": query_data,
            "hmac": hmac_digest,
            "num_pages": num_pages,
            "page_length": page_length,
            "loading_edge_pages": loading_edge_pages,
            "displayed_fields": displayed_fields,
            "hidden_fields": hidden_fields,
            "transmitted_fields": transmitted_fields,
            "field_order": field_order,
            "css_classes": css_classes,
            "display_thead": display_thead,
            "enforce_security": enforce_security,
            "generated_by": generated_by,
            "templates": templates,
        },
    )
    return context


def create_uid_from_user(request, location_identifier):
    if request.user.is_authenticated:
        return f"{request.user.pk}~{location_identifier}"
    else:
        return None


def get_page_from_row(context, row):
    return math.floor(row / context.page_length)


def view(uid, current_page, request):
    """
    Retrieves a set of pages from a context instance.
    """
    if current_page < 0:
        raise ValueError("current_page must not be negative")

    context = models.Context.objects.select_related("generated_by").get(uid=uid)

    if not context.has_permissions(request):
        raise SuspiciousOperation("User does not have access to hypercells context")

    query_data = context.query
    secret_key = getattr(settings, "SECRET_KEY", "NOTSECURE")
    hmac_digest = hmac.new(
        secret_key.encode("utf-8"), query_data, hashlib.sha256
    ).digest()
    if not hmac.compare_digest(hmac_digest, context.hmac):
        raise SuspiciousOperation(
            "HMAC signature does not match. This context may have been tampered with."
        )

    model = context.derive_model_class()

    length = context.page_length * context.num_pages
    start = current_page * context.page_length
    end = start + length
    qs = model.objects.all()
    qs.query = pickle.loads(query_data)
    total_pages = qs.count()
    qs = qs[start:end]

    instances = serialize("python", qs, fields=context.get_field_names())

    pages = {}

    for i in range(0, context.num_pages):
        page = instances[i * context.page_length : (i + 1) * context.page_length]
        pages[current_page + i] = page

    # Save to refresh the timestamp
    context.save()

    data = {
        "context_class": context.context_class,
        "total_pages": total_pages,
        "num_pages": context.num_pages,
        "page_length": context.page_length,
        "loading_edge_pages": context.loading_edge_pages,
        "css_classes": context.css_classes,
        "transmitted_fields": context.transmitted_fields,
        "field_order": context.field_order,
        "pages": pages,
    }

    return data


def delete_old_contexts(days=0, hours=8, minutes=0):
    time_ago = timezone.now() - timedelta(days=days, hours=hours, minutes=minutes)
    models.Context.objects.filter(timestamp__lte=time_ago).delete()


urlpatterns = [
    path("get/", views.get),
]
