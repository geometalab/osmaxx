from jinja2 import Environment, FileSystemLoader
import os

# Capture our current directory
TEMPLATES_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(os.path.dirname(__file__)), '..', 'templates'
    )
)


def render_to_string(template, context):
    j2_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), trim_blocks=True)
    return j2_env.get_template(template).render(context)
