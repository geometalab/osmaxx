from django import template
from django.template.context import RequestContext
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag(takes_context=True)
def email_body_with_single_result_link(context, output_file):
    view_context = {
        'file': output_file,
    }
    return render_to_string(
        'excerptexport/email_bodies/download_single_result.txt',
        context=view_context,
        context_instance=RequestContext(context.request),
    ).strip()
