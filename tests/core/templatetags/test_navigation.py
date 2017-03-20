import logging
from django.test import override_settings

from osmaxx.core.templatetags.navigation import siteabsoluteurl, logger


@override_settings(
    OSMAXX=dict(
    )
)
def test_siteabsoluteurl_without_secured_proxy_adds_scheme_and_netloc_and_path_prefix(rf, mocker):
    relative_url = 'foo/bar'
    request = rf.get('/another/path')
    logger.setLevel(logging.WARNING)
    w = mocker.patch.object(logger, 'warning')
    assert siteabsoluteurl(relative_url, request) == 'http://testserver/another/foo/bar'
    w.assert_not_called()


@override_settings(
    OSMAXX=dict(
    )
)
def test_siteabsoluteurl_without_secured_proxy_adds_scheme_and_netloc(rf, mocker):
    netloc_relative_url = '/foo/bar'
    request = rf.get('/another/path')
    logger.setLevel(logging.WARNING)
    w = mocker.patch.object(logger, 'warning')
    assert siteabsoluteurl(netloc_relative_url, request) == 'http://testserver/foo/bar'
    w.assert_not_called()


@override_settings(
    OSMAXX=dict(
    )
)
def test_siteabsoluteurl_without_secured_proxy_adds_scheme(rf, mocker):
    scheme_relative_url = '//example.com/foo/bar'
    request = rf.get('/another/path')
    logger.setLevel(logging.WARNING)
    w = mocker.patch.object(logger, 'warning')
    assert siteabsoluteurl(scheme_relative_url, request) == 'http://example.com/foo/bar'
    w.assert_not_called()


@override_settings(
    OSMAXX=dict(
    )
)
def test_siteabsoluteurl_without_secured_proxy_returns_absolute_http_urls_unchanged(rf, mocker):
    absolute_url = 'http://example.com/foo/bar'
    request = rf.get('/another/path')
    logger.setLevel(logging.WARNING)
    w = mocker.patch.object(logger, 'warning')
    assert siteabsoluteurl(absolute_url, request) == 'http://example.com/foo/bar'
    w.assert_not_called()


@override_settings(
    OSMAXX=dict(
    )
)
def test_siteabsoluteurl_without_secured_proxy_returns_absolute_https_urls_unchanged(rf, mocker):
    absolute_url = 'https://example.com/foo/bar'
    request = rf.get('/another/path')
    logger.setLevel(logging.WARNING)
    w = mocker.patch.object(logger, 'warning')
    assert siteabsoluteurl(absolute_url, request) == 'https://example.com/foo/bar'
    w.assert_not_called()


@override_settings(
    OSMAXX=dict(
    )
)
def test_siteabsoluteurl_without_secured_proxy_returns_absolute_nonhttp_urls_unchanged(rf, mocker):
    absolute_url = 'ftp://example.com/foo/bar'
    request = rf.get('/another/path')
    logger.setLevel(logging.WARNING)
    w = mocker.patch.object(logger, 'warning')
    assert siteabsoluteurl(absolute_url, request) == 'ftp://example.com/foo/bar'
    w.assert_not_called()


@override_settings(
    OSMAXX=dict(
        SECURED_PROXY=True,
    )
)
def test_siteabsoluteurl_when_secured_proxy_in_use_adds_https_and_netloc_and_path_prefix(rf, mocker):
    relative_url = 'foo/bar'
    request = rf.get('/another/path')
    logger.setLevel(logging.WARNING)
    w = mocker.patch.object(logger, 'warning')
    assert siteabsoluteurl(relative_url, request) == 'https://testserver/another/foo/bar'
    w.assert_not_called()


@override_settings(
    OSMAXX=dict(
        SECURED_PROXY=True,
    )
)
def test_siteabsoluteurl_when_secured_proxy_in_use_adds_https_and_netloc(rf, mocker):
    netloc_relative_url = '/foo/bar'
    request = rf.get('/another/path')
    logger.setLevel(logging.WARNING)
    w = mocker.patch.object(logger, 'warning')
    assert siteabsoluteurl(netloc_relative_url, request) == 'https://testserver/foo/bar'
    w.assert_not_called()


@override_settings(
    OSMAXX=dict(
        SECURED_PROXY=True,
    )
)
def test_siteabsoluteurl_when_secured_proxy_in_use_adds_https(rf, mocker):
    scheme_relative_url = '//example.com/foo/bar'
    request = rf.get('/another/path')
    logger.setLevel(logging.WARNING)
    w = mocker.patch.object(logger, 'warning')
    assert siteabsoluteurl(scheme_relative_url, request) == 'https://example.com/foo/bar'
    w.assert_not_called()


@override_settings(
    OSMAXX=dict(
        SECURED_PROXY=True,
    )
)
def test_siteabsoluteurl_when_secured_proxy_in_use_returns_absolute_http_urls_converted_to_https(rf, mocker):
    absolute_url = 'http://example.com/foo/bar'
    request = rf.get('/another/path')
    logger.setLevel(logging.WARNING)
    w = mocker.patch.object(logger, 'warning')
    assert siteabsoluteurl(absolute_url, request) == 'https://example.com/foo/bar'
    w.assert_not_called()


@override_settings(
    OSMAXX=dict(
        SECURED_PROXY=True,
    )
)
def test_siteabsoluteurl_when_secured_proxy_in_use_returns_absolute_https_urls_unchanged(rf, mocker):
    absolute_url = 'https://example.com/foo/bar'
    request = rf.get('/another/path')
    logger.setLevel(logging.WARNING)
    w = mocker.patch.object(logger, 'warning')
    assert siteabsoluteurl(absolute_url, request) == 'https://example.com/foo/bar'
    w.assert_not_called()


@override_settings(
    OSMAXX=dict(
        SECURED_PROXY=True,
    )
)
def test_siteabsoluteurl_when_secured_proxy_in_use_returns_absolute_nonhttp_urls_unchanged(rf, mocker):
    absolute_url = 'ftp://example.com/foo/bar'
    request = rf.get('/another/path')
    logger.setLevel(logging.WARNING)
    w = mocker.patch.object(logger, 'warning')
    assert siteabsoluteurl(absolute_url, request) == 'ftp://example.com/foo/bar'
    w.assert_called_with("ftp://example.com/foo/bar has not been converted to HTTPS, because it isn't an HTTP URL.")
