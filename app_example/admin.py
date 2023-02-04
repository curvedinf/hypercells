from django.contrib import admin
from app_example.models import Person


admin.site.register(Person, admin.ModelAdmin)
