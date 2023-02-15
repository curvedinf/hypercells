"""
Copyright 2023 Djangoist.com 
Distributed publicly under the CC BY-NC-ND 4.0 license
https://creativecommons.org/licenses/by-nc-nd/4.0/
"""

from django.contrib import admin
from app_example.models import Person


admin.site.register(Person, admin.ModelAdmin)
