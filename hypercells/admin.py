"""
Copyright 2023 Djangoist.com 
Distributed publicly under the CC BY-NC-ND 4.0 license
https://creativecommons.org/licenses/by-nc-nd/4.0/
"""

from django.contrib import admin

from hypercells import models


admin.site.register(models.Context, admin.ModelAdmin)
