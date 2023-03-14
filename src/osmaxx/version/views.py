import os
import subprocess
from pathlib import Path

from django.conf import settings
from django.shortcuts import render


def show_version_number(request):
    print(Path(__file__).parent.parent.parent.parent.absolute())
    working_dir = os.getenv('WORKDIR', Path(__file__).parent.parent.parent.parent.absolute())
    run_process = subprocess.run('poetry version', capture_output=True, check=True, shell=True, text=True, cwd=str(working_dir))
    version = run_process.stdout.strip('\n')
    return render(
        request=request,
        template_name="version/show_version.html",
        context={
            "version_number": version,
            "DEBUG": settings.DEBUG,
        },
    )
