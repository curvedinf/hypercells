from django.contrib import admin
from django.urls import path, include

import webapp.views

urlpatterns = [
    path("", webapp.views.index),
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
]
