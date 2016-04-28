from django import template
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def email_body_with_single_result_link(context, output_file):
    view_context = {
        'file': output_file,
    }
    return mark_safe(render_to_string(
        'excerptexport/email_bodies/download_single_result.txt',
        context=view_context,
        context_instance=RequestContext(context.request),
    ).strip())


@register.simple_tag(takes_context=True)
def email_body_with_all_result_links(context, extraction_order):
    return mark_safe('\r\n'.join(
        email_body_with_single_result_link(context, file)
        for file in extraction_order.output_files.all().order_by('-file_extension')
    ))
