from django.conf import settings
from django.shortcuts import render_to_response

import osmaxx


def show_version_number(request):
    return render_to_response(template_name='version/show_version.html', context={
        'version_number': osmaxx.__version__,
        'DEBUG': settings.DEBUG,
    })
