import logging

import requests
from requests.models import CONTENT_CHUNK_SIZE

logger = logging.getLogger(__name__)


class RESTApiClient:
    """
    REST Client Base Class

    :param service_base: the base url
    """

    def __init__(self, service_base):
        self.service_base = service_base

    def get(self, url, params=None, **kwargs):
        return self._request(requests.get, url, dict(params=params), kwargs)

    def post(self, url, json_data=None, **kwargs):
        return self._request(requests.post, url, dict(json=json_data), kwargs)

    def _request(self, method, url, payload, kwargs):
        kwargs = self._data_dict(**kwargs)
        kwargs.update(payload)
        response = method(self._to_fully_qualified_url(url), **kwargs)
        response.raise_for_status()
        return response

    def _data_dict(self, **kwargs):
        headers = self._default_headers()
        if 'headers' in kwargs:
            headers.update(kwargs.pop('headers'))
        return dict(headers=headers, **kwargs)

    def _default_headers(self):
        return {
            'Content-Type': 'application/json; charset=UTF-8',
        }

    def _is_colliding_slashes(self, url):
        return self.service_base.endswith('/') and url.startswith('/')

    def _to_fully_qualified_url(self, url):
        if url.startswith('http'):
            return url
        base_url = self.service_base[:-1] if (self._is_colliding_slashes(url)) else self.service_base
        return base_url + url


class JWTClient(RESTApiClient):
    """REST client with JWT authentication

    :param login_url: the relative path to the login url
    """

    def __init__(self, *args, username, password, login_url, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = username
        self.password = password
        self.login_url = login_url
        self.token = None

    def authorized_get(self, url, params=None, **kwargs):
        return self.get(url, params, headers=self._authorization_headers(), **kwargs)

    def authorized_post(self, url, json_data=None, **kwargs):
        return self.post(url, json_data, headers=self._authorization_headers(), **kwargs)

    def _login(self):
        """
        Logs in the api client by requesting an API token
        """
        if self.token:
            # already logged in
            return
            # TODO: comply to JWT and check whether key is (still) valid, whether it needs reinitialization etc.
        login_url = self._to_fully_qualified_url(self.login_url)
        login_data = dict(username=self.username, password=self.password, next=self.service_base)
        response = self.post(login_url, json_data=login_data, headers=dict(Referer=login_url))
        self.token = response.json().get('token')
        return response

    def _authorization_headers(self):
        self._login()
        return {
            'Authorization': 'JWT {token}'.format(token=self.token),
        }


class LazyChunkedRemoteFile:
    """Wrapper around to-be-downloaded files

    Can be passed to django.core.files.storage.Storage#save as ``content``
    if that storage's save logic consumes chunks like ``FileSystemStorage`` does
    at https://github.com/django/django/blob/1.9.4/django/core/files/storage.py#L252

    Notes:
        - This is not a file-like object: It has no ``read`` method.
        - Object initialization opens the connection for downloading, but will not fetch the content until the chunks
          are requested. If too much time has passed between those steps, the server might have closed the connection,
          so don't wait too long.
    """

    def __init__(self, *args, download_function=requests.get, **kwargs):
        stream = kwargs.pop('stream', True)
        assert stream, "can't chunk without streaming"
        response = download_function(*args, stream=stream, **kwargs)
        self._content_it = response.iter_content(chunk_size=CONTENT_CHUNK_SIZE)
        self._size = 0

    def chunks(self):
        for chunk in self._content_it:
            if chunk:
                self._size += len(chunk)
                yield chunk

    @property
    def size(self):
        return self._size


def reasons_for(http_error):
    return http_error.response.json()
