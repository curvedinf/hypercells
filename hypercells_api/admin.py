from django.contrib import admin

from hypercells_api import models


class ContextAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Context, ContextAdmin)
