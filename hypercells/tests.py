"""
Copyright 2023 Djangoist.com 
Distributed publicly under the CC BY-NC-ND 4.0 license
https://creativecommons.org/licenses/by-nc-nd/4.0/
"""

import datetime
import pickle
import sys
import uuid
import json

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.exceptions import BadRequest
from django.test import RequestFactory, TestCase
from django.utils import timezone

from hypercells import lib, models, views


class LibTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser")
        self.qs = User.objects.all()
        self.context = lib.create(self.qs)
        self.factory = RequestFactory()

    def test_valid_request(self):
        request = self.factory.get(views.get, {"uid": self.context.uid, "page": "0"})
        response = views.get(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["content-type"], "application/json")

        pages = json.loads(response.content)
        self.assertIsInstance(pages, dict)
        self.assertIn("context_class", pages)
        self.assertIn("total_pages", pages)
        self.assertIn("num_pages", pages)
        self.assertIn("page_length", pages)
        self.assertIn("loading_edge_pages", pages)
        self.assertIn("css_classes", pages)
        self.assertIn("transmitted_fields", pages)
        self.assertIn("field_order", pages)
        self.assertIn("pages", pages)

    def test_missing_uid(self):
        request = self.factory.get(views.get, {"page": "0"})
        with self.assertRaises(BadRequest):
            views.get(request)

    def test_missing_page(self):
        request = self.factory.get(views.get, {"uid": "abc123"})
        with self.assertRaises(BadRequest):
            views.get(request)

    def test_invalid_page(self):
        request = self.factory.get(views.get, {"uid": "abc123", "page": "foo"})
        with self.assertRaises(BadRequest):
            views.get(request)

    def test_negative_page(self):
        request = self.factory.get(views.get, {"uid": "abc123", "page": "-1"})
        with self.assertRaises(BadRequest):
            views.get(request)

    def test_view_raises_exception(self):
        request = self.factory.get(views.get, {"uid": "nonexistent_uid", "page": "0"})
        with self.assertRaises(lib.models.Context.DoesNotExist):
            views.get(request)

    def test_create_with_queryset(self):
        queryset = models.Context.objects.all()
        result = lib.create(queryset)
        self.assertIsInstance(result, models.Context)

    def test_create_with_uid(self):
        uid = str(uuid.uuid4())
        queryset = models.Context.objects.all()
        result = lib.create(queryset, uid=uid)
        self.assertEqual(str(result.uid), uid)

    def test_create_with_display_thead(self):
        queryset = models.Context.objects.all()
        result = lib.create(queryset, display_thead=False)
        self.assertEqual(result.display_thead, False)

    def test_create_with_enforce_security(self):
        request = RequestFactory().get("/")
        request.user = User.objects.create_user(
            username="test_user",
            email="test_user@example.com",
            password="test_password",
        )
        queryset = models.Context.objects.all()
        result = lib.create(queryset, enforce_security=True, request=request)
        self.assertEqual(result.generated_by, request.user)

    def test_create_with_templates(self):
        queryset = models.Context.objects.all()
        templates = {
            "js": "test_js_template.html",
            "table": "test_table_template.html",
            "loader": "test_loader_template.html",
            "td_js": "test_td_js_template.html",
            "tr_js": "test_tr_js_template.html",
        }
        result = lib.create(queryset, templates=templates)
        self.assertEqual(result.templates, templates)

    def test_view_with_valid_context(self):
        request = RequestFactory().get(views.get)
        result = lib.view(self.context.uid, 0, request)
        self.assertIsInstance(result, dict)

    def test_view_with_negative_current_page(self):
        request = RequestFactory().get(views.get)
        with self.assertRaises(ValueError):
            lib.view(self.context.uid, -1, request)

    def test_delete_old_contexts(self):
        models.Context.objects.all().delete()
        context = lib.create(User.objects.all())
        models.Context.objects.filter(pk=context.pk).update(
            timestamp=timezone.now() - datetime.timedelta(minutes=10)
        )
        lib.delete_old_contexts(days=0, hours=0, minutes=1)
        count = models.Context.objects.count()
        self.assertEqual(count, 0)


class ContextModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser")
        self.context_data = {
            "uid": "test-uid",
            "model_module": "django.contrib.auth.models",
            "model_class": "User",
            "query": pickle.dumps(User.objects.all().query),
            "display_thead": True,
            "num_pages": 1,
            "page_length": 10,
            "loading_edge_pages": 3,
            "displayed_fields": [],
            "hidden_fields": [],
            "transmitted_fields": [],
            "field_order": [],
            "css_classes": {},
            "enforce_security": False,
            "generated_by": None,
            "templates": {},
        }

    def test_context_creation(self):
        context = models.Context.objects.create(**self.context_data)
        self.assertEqual(context.uid, self.context_data["uid"])
        self.assertEqual(context.model_module, self.context_data["model_module"])
        self.assertEqual(context.model_class, self.context_data["model_class"])
        self.assertEqual(context.query, self.context_data["query"])
        self.assertEqual(context.display_thead, self.context_data["display_thead"])
        self.assertEqual(context.num_pages, self.context_data["num_pages"])
        self.assertEqual(context.page_length, self.context_data["page_length"])
        self.assertEqual(
            context.loading_edge_pages, self.context_data["loading_edge_pages"]
        )
        self.assertEqual(
            context.displayed_fields, self.context_data["displayed_fields"]
        )
        self.assertEqual(context.hidden_fields, self.context_data["hidden_fields"])
        self.assertEqual(
            context.transmitted_fields, self.context_data["transmitted_fields"]
        )
        self.assertEqual(context.field_order, self.context_data["field_order"])
        self.assertEqual(context.css_classes, self.context_data["css_classes"])
        self.assertEqual(
            context.enforce_security, self.context_data["enforce_security"]
        )
        self.assertEqual(context.generated_by, self.context_data["generated_by"])
        self.assertEqual(context.templates, self.context_data["templates"])

    def test_context_derive_model_class(self):
        context = models.Context.objects.create(**self.context_data)
        model_class = context.derive_model_class()
        self.assertEqual(model_class, User)

    def test_context_get_fields(self):
        context = models.Context.objects.create(**self.context_data)
        fields = context.get_fields()
        self.assertTrue(isinstance(fields, list))

    def test_context_get_field_verbose_names(self):
        context = models.Context.objects.create(**self.context_data)
        field_verbose_names = context.get_field_verbose_names()
        self.assertTrue(isinstance(field_verbose_names, list))

    def test_context_get_ordered_field_verbose_names(self):
        context = models.Context.objects.create(**self.context_data)
        ordered_field_verbose_names = context.get_ordered_field_verbose_names()
        self.assertTrue(isinstance(ordered_field_verbose_names, list))

    def test_context_get_field_names(self):
        context = models.Context.objects.create(**self.context_data)
        field_names = context.get_field_names()
        self.assertTrue(isinstance(field_names, list))

    def test_context_has_permissions(self):
        context_data_with_security = self.context_data.copy()
        context_data_with_security["enforce_security"] = True
        context_data_with_security["generated_by"] = self.user

        context_data_without_security = self.context_data.copy()
        context_data_without_security["uid"] = "test-uid2"
        context_data_without_security["enforce_security"] = False

        context_with_security = models.Context.objects.create(
            **context_data_with_security
        )
        context_without_security = models.Context.objects.create(
            **context_data_without_security
        )

        request_with_user = self.client.request().wsgi_request
