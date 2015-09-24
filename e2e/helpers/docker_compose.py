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


def create_superuser_for_test(username, email=""):
    """
    password is `password` for testing purposes
    """
    superuser_fixture_yaml = """
- fields:
    date_joined: 2015-09-24 04:30:13.073706+00:00
    email: '%(email)s'
    first_name: ''
    groups: []
    is_active: true
    is_staff: true
    is_superuser: true
    last_login: null
    last_name: ''
    password: pbkdf2_sha256$20000$udZmTmpcfGYE$+hQotzuagjhSAGWnUayGjCP/f6yNHFq5ByvqTnnFp5M=
    user_permissions: []
    username: %(username)s
  model: auth.user
  pk: 1
    """ % {'email': email, 'username': username}
    subprocess.check_call(
        shlex.split(
            'docker-compose run --rm webappdev /bin/bash -c "echo \"{}\" > fixture.json;'
            './manage.py loaddata fixture.json"'.format(superuser_fixture_yaml),
            comments=True
        )
    )

__all__ = [
    stop, clean, build, pull, start, create_superuser_for_test
]
