import os
import shlex
import subprocess
from time import sleep


def stop():
    subprocess.check_call("docker-compose stop -t 0".split(' '))


def clean():
    stop()
    subprocess.check_call("docker-compose rm -vf".split(' '))


def build():
    subprocess.check_call("docker-compose build".split(' '))


def pull():
    subprocess.check_call("docker-compose pull".split(' '))


def start():
    subprocess.check_call("docker-compose up -d databasedev".split(' '))

    sleep(10)

    subprocess.check_call(
        shlex.split("docker-compose run --rm webappdev /bin/bash -c './manage.py migrate'", comments=True)
    )

    subprocess.check_call("docker-compose up -d".split(' '))


def create_superuser_for_test(username, password, email=""):
    """
    password is `password` for testing purposes
    """
    superuser_command = """from django.contrib.auth.models import User
User.objects.create_superuser(username='{username}', password='{password}', email='{email}')
    """.format(email=email, username=username, password=password)
    # FIXME: this only works on development mode with mounted source volumes
    filename = os.path.join(os.path.dirname(__file__), '..', '..', 'osmaxx-py', 'create_superuser.py')
    with open(filename, mode='w') as file:
        file.write(superuser_command)

    subprocess_command = 'docker-compose run --rm webappdev /bin/bash -c "{}"'.format(
        './manage.py runscript --silent create_superuser.py',
    )
    subprocess.check_call(
        shlex.split(
            subprocess_command,
            comments=True
        )
    )
    os.unlink(filename)

__all__ = [
    stop, clean, build, pull, start, create_superuser_for_test
]
