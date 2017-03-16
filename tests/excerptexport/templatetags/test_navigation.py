from django.test import override_settings

from osmaxx.excerptexport.templatetags.navigation import siteabsoluteurl


@override_settings(
    OSMAXX=dict(
    )
)
def test_siteabsoluteurl_without_secured_proxy_adds_scheme_and_netloc_and_path_prefix(rf):
    relative_url = 'foo/bar'
    request = rf.get('/another/path')
    assert siteabsoluteurl(relative_url, request) == 'http://testserver/another/foo/bar'


@override_settings(
    OSMAXX=dict(
    )
)
def test_siteabsoluteurl_without_secured_proxy_adds_scheme_and_netloc(rf):
    netloc_relative_url = '/foo/bar'
    request = rf.get('/another/path')
    assert siteabsoluteurl(netloc_relative_url, request) == 'http://testserver/foo/bar'


@override_settings(
    OSMAXX=dict(
    )
)
def test_siteabsoluteurl_without_secured_proxy_adds_scheme(rf):
    scheme_relative_url = '//example.com/foo/bar'
    request = rf.get('/another/path')
    assert siteabsoluteurl(scheme_relative_url, request) == 'http://example.com/foo/bar'


@override_settings(
    OSMAXX=dict(
    )
)
def test_siteabsoluteurl_without_secured_proxy_returns_absolute_http_urls_unchanged(rf):
    absolute_url = 'http://example.com/foo/bar'
    request = rf.get('/another/path')
    assert siteabsoluteurl(absolute_url, request) == 'http://example.com/foo/bar'


@override_settings(
    OSMAXX=dict(
    )
)
def test_siteabsoluteurl_without_secured_proxy_returns_absolute_https_urls_unchanged(rf):
    absolute_url = 'https://example.com/foo/bar'
    request = rf.get('/another/path')
    assert siteabsoluteurl(absolute_url, request) == 'https://example.com/foo/bar'


@override_settings(
    OSMAXX=dict(
        SECURED_PROXY=True,
    )
)
def test_siteabsoluteurl_when_secured_proxy_in_use_adds_https_and_netloc_and_path_prefix(rf):
    relative_url = 'foo/bar'
    request = rf.get('/another/path')
    assert siteabsoluteurl(relative_url, request) == 'https://testserver/another/foo/bar'


@override_settings(
    OSMAXX=dict(
        SECURED_PROXY=True,
    )
)
def test_siteabsoluteurl_when_secured_proxy_in_use_adds_https_and_netloc(rf):
    netloc_relative_url = '/foo/bar'
    request = rf.get('/another/path')
    assert siteabsoluteurl(netloc_relative_url, request) == 'https://testserver/foo/bar'


@override_settings(
    OSMAXX=dict(
        SECURED_PROXY=True,
    )
)
def test_siteabsoluteurl_when_secured_proxy_in_use_adds_https(rf):
    scheme_relative_url = '//example.com/foo/bar'
    request = rf.get('/another/path')
    assert siteabsoluteurl(scheme_relative_url, request) == 'https://example.com/foo/bar'


@override_settings(
    OSMAXX=dict(
        SECURED_PROXY=True,
    )
)
def test_siteabsoluteurl_when_secured_proxy_in_use_returns_absolute_http_urls_converted_to_https(rf):
    absolute_url = 'http://example.com/foo/bar'
    request = rf.get('/another/path')
    assert siteabsoluteurl(absolute_url, request) == 'https://example.com/foo/bar'


@override_settings(
    OSMAXX=dict(
        SECURED_PROXY=True,
    )
)
def test_siteabsoluteurl_when_secured_proxy_in_use_returns_absolute_https_urls_unchanged(rf):
    absolute_url = 'https://example.com/foo/bar'
    request = rf.get('/another/path')
    assert siteabsoluteurl(absolute_url, request) == 'https://example.com/foo/bar'
