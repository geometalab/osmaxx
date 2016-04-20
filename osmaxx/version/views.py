import importlib

from django.conf import settings
from django.shortcuts import render_to_response


def show_version_number(request):
    version = importlib.import_module('__init__').__version__
    return render_to_response(template_name='version/show_version.html', context={
        'version_number': version,
        'DEBUG': settings.DEBUG,
    })
