import os
from time import sleep
import unittest
import subprocess

try:
    import requests
except ImportError:
    requirements_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    subprocess.check_call("pip install -r {}".format(requirements_file).split(' '))
    import requests

from helpers import docker_compose

ADMIN_USER_FOR_TESTS = 'admin'


def _start_containers():
    """
    first clean up, then check for newer images and then start the containers.
    Then wait 10 seconds to be certain the webapp is up and ready to receive.
    """
    docker_compose.clean()
    docker_compose.pull()
    docker_compose.start()
    docker_compose.create_superuser_for_test(ADMIN_USER_FOR_TESTS)
    sleep(10)


def _stop_containers():
    """
    stop the containers and then cleanup
    """
    docker_compose.stop()
    docker_compose.clean()


class TestE2E(unittest.TestCase):
    # password is the default password
    COOKIES = dict()
    CSRF_TOKEN = ''
    LOGIN_PAYLOAD = {'username': ADMIN_USER_FOR_TESTS, 'password': 'password'}

    def _login(self):
        login_url = 'http://localhost:8000/login/'
        client = requests.session()
        client.get(login_url)

        csrf_token = client.cookies['csrftoken']
        login_data = {
            'password': 'password',
            'username': ADMIN_USER_FOR_TESTS,
            'csrfmiddlewaretoken': csrf_token,
        }
        r = client.post(login_url, data=login_data)
        return {'request': r, 'client': client}

    def _logout(self):
        self.DJANGO_TOKEN = {'csrfmiddlewaretoken': ''}
        return requests.get('http://localhost:8000/logout/')

    def test_server_is_running(self):
        r = requests.get('http://localhost:8000/')
        self.assertEqual(r.status_code, 200)

    def test_login_denied_without_csrf_token(self):
        r = requests.post('http://localhost:8000/login/', data=self.LOGIN_PAYLOAD)
        self.assertEqual(r.status_code, 403)

    def test_login_success_with_csrf_token(self):
        r = self._login()['request']
        self.assertEqual(r.status_code, 200)
        self._logout()


if __name__ == '__main__':
    _start_containers()
    unittest.main()
    _stop_containers()
