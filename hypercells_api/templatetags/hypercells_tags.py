from django import template
from django.template.loader import get_template


register = template.Library()

@register.inclusion_tag("hypercells_js.html")
def hypercells_js(url_prefix):
    return {"url_prefix": url_prefix}

@register.inclusion_tag("hypercells_table.html")
def hypercells_table(context):
    model = context.derive_model_class()
    fields = model._meta.get_fields()
    field_names = [field.verbose_name for field in fields if field.verbose_name != "ID"]
    return {"context": context, "field_names": field_names}

@register.inclusion_tag("hypercells_loader.html")
def hypercells_loader():
    return {}
