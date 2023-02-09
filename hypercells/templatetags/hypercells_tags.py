from django import template
from django.template.loader import get_template

import hypercells.lib

register = template.Library()


def render_template_to_string(context, template_filename, template_args):
    template = context.template.engine.get_template(template_filename)
    new_context = context.new(template_args)
    csrf_token = context.get("csrf_token")
    if csrf_token is not None:
        new_context["csrf_token"] = csrf_token
    return template.render(new_context)


@register.simple_tag(takes_context=True)
def hypercells_js(context, url_prefix, hc_context=None):
    template_filename = hypercells.lib.get_template_from_context(
        hc_context, hypercells.lib.HC_TEMPLATE_JS
    )
    return render_template_to_string(
        context, template_filename, {"url_prefix": url_prefix}
    )


@register.simple_tag(takes_context=True)
def hypercells_table(context, hc_context):
    template_filename = hypercells.lib.get_template_from_context(
        hc_context, hypercells.lib.HC_TEMPLATE_TABLE
    )
    return render_template_to_string(
        context,
        template_filename,
        {
            "context": hc_context,
            "field_names": hc_context.get_field_verbose_names(),
        },
    )


@register.simple_tag(takes_context=True)
def hypercells_loader(context, hc_context=None):
    template_filename = hypercells.lib.get_template_from_context(
        hc_context, hypercells.lib.HC_TEMPLATE_LOADER
    )
    return render_template_to_string(context, template_filename, {})


@register.simple_tag(takes_context=True)
def hypercells_td_js(context, hc_context=None):
    template_filename = hypercells.lib.get_template_from_context(
        hc_context, hypercells.lib.HC_TEMPLATE_TD_JS
    )
    return render_template_to_string(context, template_filename, {})
