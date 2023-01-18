import math

from django.utils import timezone
from django.forms.models import model_to_dict

from hypercells_api import models


def create(uid, queryset, num_pages=3, page_length=100, reload_page=6):
    context, created = models.Context.objects.update_or_create(
        uid=f"{uid}",
        defaults={
            "model_module": f"{queryset.model.__module__}",
            "model_class": f"{queryset.model.__qualname__}",
            "query": f"{queryset._query}",
            "query_len": queryset.count(),
            "num_pages": num_pages,
            "page_length": page_length,
            "reload_page": reload_page,
            "data_start_page": 0,
            "data": "",
            "data_time": timezone.now,
        },
    )
    return context


def get_page_from_row(context, row):
    return math.floor(row / context.page_length)


def view(uid, viewport_row):
    context = models.Context.objects.get(uid=uid)

    current_page = get_page_from_row(context, viewport_row)

    # get the class of the context's query
    model = context.derive_model_class()

    limit = context.page_length * context.num_pages
    offset = context.data_start_page * context.page_length
    sql = f"{context.query} LIMIT {limit} OFFSET {offset}"
    qs = model.objects.raw(sql)

    data_list = []
    for instance in qs:
        data_list.append(model_to_dict(instance))

    return qs


# LIMIT 100 OFFSET 100
