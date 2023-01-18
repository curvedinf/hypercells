from django import template
from django.template.loader import get_template


register = template.Library()

# Gets the name of the passed in field on the passed in object
@register.filter
def verbose_name(context, field):
    model = context.derive_model_class()
    return 


@register.inclusion_tag("hypercells_js.html")
def hypercells_js():
    return {}


@register.inclusion_tag("hypercells_thead.html")
def hypercells_thead(context):
    model = context.derive_model_class()
    fields = model._meta.get_fields()
    field_names = [field.verbose_name for field in fields if field.verbose_name != "ID"]
    return {"context": context, "field_names": field_names}

@register.inclusion_tag("hypercells_table.html")
def hypercells_table(context):
    return {"context": context}
