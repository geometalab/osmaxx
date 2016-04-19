import pytest


def pytest_addoption(parser):
    parser.addoption("--runslow", action="store_true",
                     help="run slow tests")
    parser.addoption("--transactional", action="store_true",
                     help="run transactional db tests "
                          "(skipped by default to avoid https://code.djangoproject.com/ticket/25251) ")


# Workaround for https://code.djangoproject.com/ticket/25251
# Skip all transactional tests unless they are explicitly requested:
@pytest.fixture
def transactional_db(request, _django_db_setup, _django_cursor_wrapper):
    if request.config.getoption('--transactional'):
        from pytest_django.fixtures import transactional_db
        return transactional_db(request, _django_db_setup, _django_cursor_wrapper)
    else:
        pytest.skip()
