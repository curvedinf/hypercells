import math

from django.urls import path
from django.utils import timezone
from django.forms.models import model_to_dict
from django.core.serializers import serialize

from hypercells_api import models, views


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


def view(uid, current_page):    
    context = models.Context.objects.get(uid=uid)
    context.save()
    model = context.derive_model_class()

    limit = context.page_length * context.num_pages
    offset = current_page * context.page_length
    sql = f"{context.query} LIMIT {limit} OFFSET {offset}"
    qs = model.objects.raw(sql)
    
    instances = serialize('python', qs)
    
    pages = {}
    
    for i in range(0,context.num_pages):
        page_num = current_page + i
        page = instances[i*context.page_length : (i+1)*context.page_length]
        pages[page_num] = page
    
    return pages

urlpatterns = [
    path('get/', views.get),
]
