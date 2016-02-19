# pylint: disable=C0111
import os
from datetime import timedelta

import pytest

test_data_dir = os.path.join(os.path.dirname(__file__), 'test_data')


def pytest_configure():
    from django.conf import settings

    settings.configure(
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={'default': {'ENGINE': 'django.contrib.gis.db.backends.spatialite',
                               'NAME': ':memory:'}},
        SITE_ID=1,
        SECRET_KEY='not very secret in tests',
        USE_I18N=True,
        USE_L10N=True,
        STATIC_URL='/static/',
        ROOT_URLCONF='tests.urls',
        TEMPLATE_LOADERS=(
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ),
        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ),
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',

            'rest_framework',
            'rest_framework_gis',
            'rest_framework.authtoken',
            'tests',

            'osmaxx.clipping_area',
            'osmaxx.conversion',
        ),
        PASSWORD_HASHERS=(
            'django.contrib.auth.hashers.SHA1PasswordHasher',
            'django.contrib.auth.hashers.PBKDF2PasswordHasher',
            'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
            'django.contrib.auth.hashers.BCryptPasswordHasher',
            'django.contrib.auth.hashers.MD5PasswordHasher',
            'django.contrib.auth.hashers.CryptPasswordHasher',
        ),
        RQ_QUEUES={
            'default': {
                'HOST': 'localhost',
                'PORT': 6379,
                'DB': 0,
                'PASSWORD': '',
                'DEFAULT_TIMEOUT': 3600,
            },
        },
        JWT_AUTH={
            'JWT_ENCODE_HANDLER': 'rest_framework_jwt.utils.jwt_encode_handler',
            'JWT_DECODE_HANDLER': 'rest_framework_jwt.utils.jwt_decode_handler',
            'JWT_PAYLOAD_HANDLER': 'rest_framework_jwt.utils.jwt_payload_handler',
            'JWT_PAYLOAD_GET_USER_ID_HANDLER': 'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',
            'JWT_RESPONSE_PAYLOAD_HANDLER': 'rest_framework_jwt.utils.jwt_response_payload_handler',

            'JWT_ALGORITHM': 'HS256',
            'JWT_VERIFY': True,
            'JWT_VERIFY_EXPIRATION': True,
            'JWT_LEEWAY': 0,
            'JWT_EXPIRATION_DELTA': timedelta(seconds=300),
            'JWT_AUDIENCE': None,
            'JWT_ISSUER': None,

            'JWT_ALLOW_REFRESH': False,
            'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7),

            'JWT_AUTH_HEADER_PREFIX': 'JWT',
        },
        OSMAXX_CONVERSION_SERVICE={
            'PBF_PLANET_FILE_PATH': os.path.join(test_data_dir, 'osm', 'monaco-latest.osm.pbf'),
            'COUNTRIES_POLYFILE_LOCATION': os.path.join(test_data_dir, 'polyfiles'),
        },

    )


# if any global fixtures are needed, add them below

@pytest.fixture
def authenticated_client(client):
    """
    Client fixture using an authenticated user.

    Since this fixture creates a database object, you must
    mark your test with @pytest.mark.django_db()


    Args:
        client: Default client fixture from pytest-django

    Returns:
        Authenticated Client
    """
    from django.contrib.auth import get_user_model
    get_user_model().objects.create_user(username='lauren', password='lauri', email=None)
    client.login(username='lauren', password='lauri')
    return client


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def api_client_authenticated(api_client):
    """
    API-Client fixture using an authenticated user.

    Since this fixture creates a database object, you must
    mark your test with @pytest.mark.django_db()


    Args:
        api_client: api-client fixture

    Returns:
        Authenticated Client
    """
    return authenticated_client(api_client)


@pytest.fixture
def persisted_valid_clipping_area():
    from django.contrib.gis.geos import Polygon, MultiPolygon
    from osmaxx.clipping_area.models import ClippingArea
    poly_1 = Polygon(((0, 0), (0, 1), (1, 1), (0, 0)))
    poly_2 = Polygon(((1, 1), (1, 2), (2, 2), (1, 1)))
    multi_polygon = MultiPolygon(poly_1, poly_2)
    persisted_valid_clipping_area = ClippingArea.objects.create(name='test', clipping_multi_polygon=multi_polygon)
    assert persisted_valid_clipping_area.osmosis_polygon_file_string != ''
    assert str(persisted_valid_clipping_area) == "test (1)"
    return persisted_valid_clipping_area
