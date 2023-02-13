from django.contrib import admin
from django.urls import path, include

import hypercells.lib

import app_example.views

urlpatterns = [
    path("", app_example.views.index),
    path("basic/", app_example.views.basic),
    path("multiple/", app_example.views.multiple),
    path("cards/", app_example.views.cards),
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("hypercells/", include(hypercells.lib.urlpatterns)),
]
