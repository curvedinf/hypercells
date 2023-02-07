import math
import pickle
import uuid

from django.urls import path
from django.utils import timezone
from django.forms.models import model_to_dict
from django.core.serializers import serialize

from hypercells import models, views


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
    css_classes={
        'table': 'table table-responsive table-hover',
        'thead': '',
        'thead_tr': '',
        'thead_th': '',
        'tbody': '',
        'tbody_tr': '',
        'tbody_td': '',
    },
):
    '''
    Creates or replaces a hypercells context in the database. A context
    stores the configuration for a hypercells instance, including the 
    queryset that will drive it and other options.
    '''
    if uid is None:
        uid = uuid.uuid4()
    context, created = models.Context.objects.update_or_create(
        uid=f"{uid}",
        defaults={
            "model_module": f"{queryset.model.__module__}",
            "model_class": f"{queryset.model.__qualname__}",
            "context_class": context_class,
            "query": pickle.dumps(queryset.query),
            "num_pages": num_pages,
            "page_length": page_length,
            "loading_edge_pages": loading_edge_pages,
            "displayed_fields": displayed_fields,
            "hidden_fields": hidden_fields,
            "css_classes": css_classes,
            "display_thead": display_thead,
        },
    )
    return context

def create_uid_from_user(request, location_identifier):
    if request.user.is_authenticated:
        return f'{request.user.pk}~{location_identifier}'
    else:
        return None

def get_page_from_row(context, row):
    return math.floor(row / context.page_length)


def view(uid, current_page):
    if current_page < 0:
        raise ValueError("current_page must not be negative")

    context = models.Context.objects.get(uid=uid)
    context.save()
    model = context.derive_model_class()

    length = context.page_length * context.num_pages
    start = current_page * context.page_length
    end = start + length
    qs = model.objects.all()
    qs.query = pickle.loads(context.query)
    total_pages = qs.count()
    qs = qs[start:end]

    instances = serialize("python", qs, fields=context.get_field_names())

    pages = {}

    for i in range(0, context.num_pages):
        page = instances[i * context.page_length : (i + 1) * context.page_length]
        pages[current_page + i] = page

    data = {
        "context_class": context.context_class,
        "total_pages": total_pages,
        "num_pages": context.num_pages,
        "page_length": context.page_length,
        "loading_edge_pages": context.loading_edge_pages,
        "css_classes": context.css_classes,
        "pages": pages,
    }

    return data


urlpatterns = [
    path("get/", views.get),
]
