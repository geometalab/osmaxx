import subprocess

from django.conf import settings
from django.shortcuts import render


def show_version_number(request):
    from osmaxx import __version__

    return render(
        request=request,
        template_name="version/show_version.html",
        context={
            "version_number": __version__,
            "DEBUG": settings.DEBUG,
        },
    )
