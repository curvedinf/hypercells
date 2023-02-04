from django.contrib import admin

from hypercells import models


admin.site.register(models.Context, admin.ModelAdmin)
