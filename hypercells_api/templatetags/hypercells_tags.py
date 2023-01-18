from django import template
from django.template.loader import get_template


register = template.Library()

# Gets the name of the passed in field on the passed in object
@register.filter
def verbose_name(context, field):
    cls = context.derive_model_class()
    return cls._meta.get_field(str(field)).verbose_name


@register.inclusion_tag("hypercells_js.html")
def hypercells_js():
    return {}


@register.inclusion_tag("hypercells_thead.html")
def hypercells_thead(context, row):
    return {"context": context, "row": row}


@register.inclusion_tag("hypercells_tbody.html")
def hypercells_tbody(row):
    return {"row": row}


@register.inclusion_tag("hypercells_table.html")
def hypercells_table(context, rows):
    return {"context": context, "row": row}
