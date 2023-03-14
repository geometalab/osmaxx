from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def email_body_with_single_result_link(context, output_file, available_until):
    view_context = {
        'file': output_file,
        'available_until': available_until,
    }
    return mark_safe(render_to_string(
        'excerptexport/email/download_single_result_body.txt',
        context=view_context,
        request=context.request,
    ).strip())


@register.simple_tag(takes_context=True)
def email_body_with_all_result_links(context, extraction_order):
    return mark_safe('\r\n'.join(
        email_body_with_single_result_link(context, export.output_file)
        for export in extraction_order.exports.filter(output_file__isnull=False).order_by('file_format')
    ))
