"""
Copyright 2023 Djangoist.com 
Distributed publicly under the CC BY-NC-ND 4.0 license
https://creativecommons.org/licenses/by-nc-nd/4.0/
"""

import string, sys

from django.db import models
from django.utils import timezone
from django.conf import settings


class Context(models.Model):
    uid = models.CharField(max_length=100, unique=True, db_index=True)
    context_class = models.CharField(max_length=50)
    model_module = models.CharField(max_length=300)
    model_class = models.CharField(max_length=100)
    query = models.BinaryField()
    display_thead = models.BooleanField()
    num_pages = models.IntegerField()
    page_length = models.IntegerField()
    loading_edge_pages = models.IntegerField()
    displayed_fields = models.JSONField()
    hidden_fields = models.JSONField()
    transmitted_fields = models.JSONField()
    field_order = models.JSONField()
    css_classes = models.JSONField()
    enforce_security = models.BooleanField()
    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )
    timestamp = models.DateTimeField(auto_now=True)
    templates = models.JSONField()

    def derive_model_class(self):
        return getattr(sys.modules[str(self.model_module)], str(self.model_class))

    def get_fields(self):
        model = self.derive_model_class()
        fields = model._meta.get_fields()
        return_fields = None
        if len(self.displayed_fields) > 0:
            return_fields = [
                field
                for field in fields
                if (field.name in self.displayed_fields) and field.name != "id"
            ]
        elif len(self.hidden_fields) > 0:
            return_fields = [
                field
                for field in fields
                if (field.name not in self.hidden_fields) and field.name != "id"
            ]
        else:
            return_fields = [field for field in fields if field.name != "id"]

        if len(self.transmitted_fields) > 0:
            extra_fields = [
                field
                for field in fields
                if (field.name in self.transmitted_fields)
                and (field.name not in return_fields)
            ]
            return_fields.extend(extra_fields)

        return return_fields

    def get_field_verbose_names(self):
        fields = self.get_fields()
        return [
            field.verbose_name if hasattr(field, "verbose_name") else field.name
            for field in fields
        ]

    def get_ordered_field_verbose_names(self):
        fields = self.get_fields()
        preordered_fields = {}
        unordered_fields = []
        for field in fields:
            if field.name in self.field_order:
                preordered_fields[field.name] = field
            else:
                unordered_fields.append(field)
        ordered_fields = []
        for field_name in self.field_order:
            if field_name in preordered_fields:
                ordered_fields.append(preordered_fields[field_name])
        ordered_fields.extend(unordered_fields)
        return [
            field.verbose_name if hasattr(field, "verbose_name") else field.name
            for field in ordered_fields
        ]

    def get_field_names(self):
        fields = self.get_fields()
        return [field.name for field in fields]

    def has_permissions(self, request):
        if not self.enforce_security:
            return True
        if self.generated_by == None:  # anonymous users
            return True
        return self.generated_by == request.user

    def __str__(self):
        return self.uid
