import random, string, sys

from django.db import models
from django.utils import timezone


def random_uid():
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(10))


class Context(models.Model):
    uid = models.CharField(max_length=100, unique=True, db_index=True)
    model_module = models.CharField(max_length=200)
    model_class = models.CharField(max_length=100)
    query = models.TextField()
    query_len = models.IntegerField()
    num_pages = models.IntegerField()
    page_length = models.IntegerField()
    reload_page = models.IntegerField()  # relative to data_start_page
    data_start_page = models.IntegerField()
    data = models.JSONField(blank=True, null=True)
    data_time = models.DateTimeField(default=timezone.now)

    def derive_model_class(self):
        return getattr(sys.modules[str(self.model_module)], str(self.model_class))
