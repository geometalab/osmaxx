import os
from time import sleep
import unittest
import subprocess
from helpers.html_helpers import make_soup
from helpers.zip_file_helpers import check_if_result_contains_data

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    requirements_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    subprocess.check_call("pip install -r {}".format(requirements_file).split(' '))
    import requests
    from bs4 import BeautifulSoup  # noqa ignore imported but unused

from helpers import docker_compose

ADMIN_USER_FOR_TESTS = 'admin'
ADMIN_PASSWORD_FOR_TESTS = 'admin'


def _start_containers():
    """
    first clean up, then check for newer images and then start the containers.
    Then wait 10 seconds to be certain the webapp is up and ready to receive.
    """
    docker_compose.clean()
    docker_compose.pull()
    docker_compose.start()
    docker_compose.create_superuser_for_test(username=ADMIN_USER_FOR_TESTS, password=ADMIN_PASSWORD_FOR_TESTS)
    sleep(10)


def _stop_containers():
    """
    stop the containers and then cleanup
    """
    # docker_compose.stop()
    # docker_compose.clean()


class TestE2E(unittest.TestCase):
    COOKIES = dict()
    CSRF_TOKEN = ''

    def _login(self, next=None):
        login_url = 'http://localhost:8000/login/'
        client = requests.session()
        client.get(login_url)

        csrf_token = client.cookies['csrftoken']
        login_data = {
            'password': ADMIN_PASSWORD_FOR_TESTS,
            'username': ADMIN_USER_FOR_TESTS,
            'csrfmiddlewaretoken': csrf_token,
            'next': next,
        }
        r = client.post(login_url, data=login_data)
        return {'request': r, 'client': client}

    def _logout(self):
        return requests.get('http://localhost:8000/logout/')

    def _make_link(self, link):
        host = 'http://localhost:8000{}'
        return host.format(link)

    def _download_and_test_zip_contents(self, client, download_link):
        download_link = self._make_link(download_link)
        r = client.get(download_link)
        check_if_result_contains_data(r.content, self.assertGreater)

    def test_server_is_running(self):
        r = requests.get('http://localhost:8000/')
        self.assertEqual(r.status_code, 200)

    def test_login_denied_without_csrf_token(self):
        login_data = {'username': ADMIN_USER_FOR_TESTS, 'password': ADMIN_PASSWORD_FOR_TESTS}
        r = requests.post('http://localhost:8000/login/', data=login_data)
        self.assertEqual(r.status_code, 403)

    def test_login_success_with_csrf_token(self):
        login = self._login(next='/orders/')
        r = login['request']
        soup = make_soup(r.content)
        self.assertIsNotNone(soup.find(name='a', attrs={'href': '/logout/?next=/'}))
        self.assertEqual(r.status_code, 200)
        self._logout()

    def test_create_new_excerpt_succeeds(self):
        client = self._login()['client']

        csrf_token = client.cookies['csrftoken']

        payload = {
            'csrfmiddlewaretoken': csrf_token,
            'form-mode': 'new-excerpt',
            'new_excerpt_name': 'HSR',
            'new_excerpt_bounding_box_north': 47.22407852727801,
            'new_excerpt_bounding_box_west': 8.815616369247437,
            'new_excerpt_bounding_box_east': 8.819221258163452,
            'new_excerpt_bounding_box_south': 47.222388077452706,
            'export_options.GisExcerptConverter.formats': [
                'spatialite',
                'gpkg',
                'shp',
            ],
        }
        r = client.post('http://localhost:8000/orders/new/', data=payload)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.history[0].status_code, 302)

        # check_generated_content

        print("It is running, but waiting for 5 minutes to wait for the process to finish! "
              "Please be patient and get a coffee. ;-)")

        sleep(5*60)  # five minutes; generating should be done after that

        r = client.get(self._make_link('/orders/'))
        soup = make_soup(r.content)

        link = self._make_link(soup.find(attrs={'class': 'container-row content'}).a.attrs['href'])

        r = client.get(link)
        soup = make_soup(r.content)

        # first link
        self._download_and_test_zip_contents(
            client,
            soup.find(name='ul', attrs={'class': 'download_files'}).find_all('a')[0].attrs['href']
        )

        # second link
        self._download_and_test_zip_contents(
            client,
            soup.find(name='ul', attrs={'class': 'download_files'}).find_all('a')[2].attrs['href']
        )

        # third link
        self._download_and_test_zip_contents(
            client,
            soup.find(name='ul', attrs={'class': 'download_files'}).find_all('a')[4].attrs['href']
        )


if __name__ == '__main__':
    _start_containers()
    unittest.main()
    _stop_containers()
