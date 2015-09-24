import os
from time import sleep
import unittest
import subprocess

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    requirements_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    subprocess.check_call("pip install -r {}".format(requirements_file).split(' '))
    import requests
    from bs4 import BeautifulSoup

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
    payload = {'username': ADMIN_USER_FOR_TESTS, 'password': 'password'}

    def test_server_is_running(self):
        r = requests.get('http://localhost:8000/')
        self.assertEqual(r.status_code, 200)

    def test_login_denied_without_csrf_token(self):
        r = requests.post('http://localhost:8000/login/', data=self.payload)
        self.assertEqual(r.status_code, 403)

    def test_login_success_with_csrf_token(self):
        r = requests.get('http://localhost:8000/login/')
        soup = BeautifulSoup(r.content, 'html.parser')

        payload = self.payload
        # TODO: this relies upon the form coming first and the first input element being the hidden csrf token
        payload['csrfmiddlewaretoken'] = soup.form.input.attrs['value']
        cookies = dict(csrftoken=soup.form.input.attrs['value'])

        r = requests.post('http://localhost:8000/login/', data=payload, cookies=cookies)
        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    _start_containers()
    unittest.main()
    _stop_containers()
