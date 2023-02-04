from django.contrib import admin
from django.urls import path, include

import hypercells.lib

import app_example.views

urlpatterns = [
    path("", app_example.views.index),
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("hypercells/", include(hypercells.lib.urlpatterns)),
]
