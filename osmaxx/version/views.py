from django.conf import settings
from django.shortcuts import render_to_response


def show_version_number(request):
    from osmaxx import __version__
    return render_to_response(template_name='version/show_version.html', context={
        'version_number': __version__,
        'DEBUG': settings.DEBUG,
    })
