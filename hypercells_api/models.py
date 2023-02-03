import string, sys

from django.db import models
from django.utils import timezone


def random_uid():
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(10))


class Context(models.Model):
    uid = models.CharField(max_length=100, unique=True, db_index=True)
    model_module = models.CharField(max_length=300)
    model_class = models.CharField(max_length=100)
    query = models.BinaryField()
    num_pages = models.IntegerField()
    page_length = models.IntegerField()
    loading_edge_pages = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)

    def derive_model_class(self):
        return getattr(sys.modules[str(self.model_module)], str(self.model_class))
