import string, sys

from django.db import models
from django.utils import timezone

# TODO: delete from migration
def random_uid():
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(10))


class Context(models.Model):
    uid = models.CharField(max_length=100, unique=True, db_index=True)
    context_class = models.CharField(max_length=50)
    model_module = models.CharField(max_length=300)
    model_class = models.CharField(max_length=100)
    query = models.BinaryField()
    num_pages = models.IntegerField()
    page_length = models.IntegerField()
    loading_edge_pages = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)
    displayed_fields = models.JSONField()
    hidden_fields = models.JSONField()

    def derive_model_class(self):
        return getattr(sys.modules[str(self.model_module)], str(self.model_class))

    def get_fields(self):
        model = self.derive_model_class()
        fields = model._meta.get_fields()
        if len(self.displayed_fields) > 0:
            return [
                field
                for field in fields
                if (field.name in self.displayed_fields) and field.name != "id"
            ]
        if len(self.hidden_fields) > 0:
            return [
                field
                for field in fields
                if (field.name not in self.hidden_fields) and field.name != "id"
            ]
        return [field for field in fields if field.name != "id"]

    def get_field_verbose_names(self):
        fields = self.get_fields()
        return [field.verbose_name for field in fields]

    def get_field_names(self):
        fields = self.get_fields()
        return [field.name for field in fields]

    def __str__(self):
        return self.uid