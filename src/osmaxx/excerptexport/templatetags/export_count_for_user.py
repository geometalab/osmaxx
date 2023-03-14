from django import template

register = template.Library()


@register.simple_tag(takes_context=False)
def export_count_for_user(user, excerpt):
    return excerpt.attached_export_count(user=user)
