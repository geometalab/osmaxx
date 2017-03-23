import logging

import pytest
from django.test import override_settings

from osmaxx.core.templatetags.navigation import siteabsoluteurl, logger


@override_settings(
    OSMAXX=dict(
    )
)
def test_siteabsoluteurl_without_secured_proxy_adds_scheme_and_netloc_and_path_prefix(rf, log_warning_mock):
    relative_url = 'foo/bar'
    request = rf.get('/another/path')
    assert siteabsoluteurl(relative_url, request) == 'http://testserver/another/foo/bar'
    log_warning_mock.assert_not_called()


@override_settings(
    OSMAXX=dict(
    )
)
def test_siteabsoluteurl_without_secured_proxy_adds_scheme_and_netloc(rf, log_warning_mock):
    netloc_relative_url = '/foo/bar'
    request = rf.get('/another/path')
    assert siteabsoluteurl(netloc_relative_url, request) == 'http://testserver/foo/bar'
    log_warning_mock.assert_not_called()


@override_settings(
    OSMAXX=dict(
    )
)
def test_siteabsoluteurl_without_secured_proxy_adds_scheme(rf, log_warning_mock):
    scheme_relative_url = '//example.com/foo/bar'
    request = rf.get('/another/path')
    assert siteabsoluteurl(scheme_relative_url, request) == 'http://example.com/foo/bar'
    log_warning_mock.assert_not_called()


@override_settings(
    OSMAXX=dict(
    )
)
def test_siteabsoluteurl_without_secured_proxy_returns_absolute_http_urls_unchanged(rf, log_warning_mock):
    absolute_url = 'http://example.com/foo/bar'
    request = rf.get('/another/path')
    assert siteabsoluteurl(absolute_url, request) == 'http://example.com/foo/bar'
    log_warning_mock.assert_not_called()


@override_settings(
    OSMAXX=dict(
    )
)
def test_siteabsoluteurl_without_secured_proxy_returns_absolute_https_urls_unchanged(rf, log_warning_mock):
    absolute_url = 'https://example.com/foo/bar'
    request = rf.get('/another/path')
    assert siteabsoluteurl(absolute_url, request) == 'https://example.com/foo/bar'
    log_warning_mock.assert_not_called()


@override_settings(
    OSMAXX=dict(
    )
)
def test_siteabsoluteurl_without_secured_proxy_returns_absolute_nonhttp_urls_unchanged(rf, log_warning_mock):
    absolute_url = 'ftp://example.com/foo/bar'
    request = rf.get('/another/path')
    assert siteabsoluteurl(absolute_url, request) == 'ftp://example.com/foo/bar'
    log_warning_mock.assert_not_called()


@override_settings(
    OSMAXX=dict(
        SECURED_PROXY=True,
    )
)
def test_siteabsoluteurl_when_secured_proxy_in_use_adds_https_and_netloc_and_path_prefix(rf, log_warning_mock):
    relative_url = 'foo/bar'
    request = rf.get('/another/path')
    assert siteabsoluteurl(relative_url, request) == 'https://testserver/another/foo/bar'
    log_warning_mock.assert_not_called()


@override_settings(
    OSMAXX=dict(
        SECURED_PROXY=True,
    )
)
def test_siteabsoluteurl_when_secured_proxy_in_use_adds_https_and_netloc(rf, log_warning_mock):
    netloc_relative_url = '/foo/bar'
    request = rf.get('/another/path')
    assert siteabsoluteurl(netloc_relative_url, request) == 'https://testserver/foo/bar'
    log_warning_mock.assert_not_called()


@override_settings(
    OSMAXX=dict(
        SECURED_PROXY=True,
    )
)
def test_siteabsoluteurl_when_secured_proxy_in_use_adds_https(rf, log_warning_mock):
    scheme_relative_url = '//example.com/foo/bar'
    request = rf.get('/another/path')
    assert siteabsoluteurl(scheme_relative_url, request) == 'https://example.com/foo/bar'
    log_warning_mock.assert_not_called()


@override_settings(
    OSMAXX=dict(
        SECURED_PROXY=True,
    )
)
def test_siteabsoluteurl_when_secured_proxy_in_use_returns_absolute_http_urls_converted_to_https(rf, log_warning_mock):
    absolute_url = 'http://example.com/foo/bar'
    request = rf.get('/another/path')
    assert siteabsoluteurl(absolute_url, request) == 'https://example.com/foo/bar'
    log_warning_mock.assert_not_called()


@override_settings(
    OSMAXX=dict(
        SECURED_PROXY=True,
    )
)
def test_siteabsoluteurl_when_secured_proxy_in_use_returns_absolute_https_urls_unchanged(rf, log_warning_mock):
    absolute_url = 'https://example.com/foo/bar'
    request = rf.get('/another/path')
    assert siteabsoluteurl(absolute_url, request) == 'https://example.com/foo/bar'
    log_warning_mock.assert_not_called()


@override_settings(
    OSMAXX=dict(
        SECURED_PROXY=True,
    )
)
def test_siteabsoluteurl_when_secured_proxy_in_use_returns_absolute_nonhttp_urls_unchanged(rf, log_warning_mock):
    absolute_url = 'ftp://example.com/foo/bar'
    request = rf.get('/another/path')
    assert siteabsoluteurl(absolute_url, request) == 'ftp://example.com/foo/bar'
    log_warning_mock.assert_called_with(
        "ftp://example.com/foo/bar has not been converted to HTTPS, because it isn't an HTTP URL.")


@pytest.yield_fixture
def log_warning_mock(mocker):
    original_level = logger.level
    logger.setLevel(logging.WARNING)
    yield mocker.patch.object(logger, 'warning')
    logger.setLevel(original_level)
