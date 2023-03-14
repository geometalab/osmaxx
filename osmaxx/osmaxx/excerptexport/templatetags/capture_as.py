# Adapted from https://www.djangosnippets.org/snippets/545/
from django import template

register = template.Library()


@register.tag(name='capture_as')
def do_capture_as(parser, token):
    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("'capture_as' node requires a variable name.")
    nodelist = parser.parse(('end_capture_as',))
    parser.delete_first_token()
    return CaptureAsNode(nodelist, args)


class CaptureAsNode(template.Node):
    def __init__(self, nodelist, varname):
        self.nodelist = nodelist
        self.varname = varname

    def render(self, context):
        output = self.nodelist.render(context)
        context[self.varname] = output
        return ''
