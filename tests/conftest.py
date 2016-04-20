# pylint: disable=C0111
import os
import tempfile
from datetime import timedelta

import pytest

test_data_dir = os.path.join(os.path.dirname(__file__), 'test_data')

postgres_container_userland_port = 65432  # required for travis, so using it everywhere


def pytest_configure():
    from django.conf import settings

    settings.configure(
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.contrib.gis.db.backends.postgis',
                'NAME': 'postgres',
                'USER': 'postgres',
                'PASSWORD': 'postgres',
                'PORT': '54321',
                'HOST': '127.0.0.1',
            }
        },
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
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'OPTIONS': {
                    'context_processors': [
                        'django.contrib.auth.context_processors.auth',
                        'django.template.context_processors.debug',
                        'django.template.context_processors.i18n',
                        'django.template.context_processors.media',
                        'django.template.context_processors.static',
                        'django.template.context_processors.tz',
                        'django.template.context_processors.request',
                    ],
                    'loaders': [
                        'django.template.loaders.filesystem.Loader',
                        'django.template.loaders.app_directories.Loader',
                    ]
                },
            },
        ],
        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'osmaxx.job_progress.middleware.OrderUpdaterMiddleware',
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
            'crispy_forms',

            'tests',

            # conversion service apps
            'osmaxx.clipping_area',
            'osmaxx.conversion',

            # web_frontend apps
            'osmaxx.countries',
            'osmaxx.excerptexport',
            'osmaxx.job_progress',
            'osmaxx.social_auth',

            # special model for testing only
            'tests.utilities.test_models',
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
        },
        _OSMAXX_POLYFILE_LOCATION=os.path.join(test_data_dir, 'polyfiles'),

        # Some of our tests erase PRIVATE_MEDIA_ROOT dir to clean up after themselves,
        # so DON'T set this to the location of anything valuable.
        PRIVATE_MEDIA_ROOT=tempfile.mkdtemp(),

        OSMAXX_TEST_SETTINGS={
            'download_file_name': '%(excerpt_name)s-%(content_type)s-%(id)s.%(file_extension)s',
            'CONVERSION_SERVICE_URL': 'http://localhost:8901/api/',
            'CONVERSION_SERVICE_USERNAME': 'dev',
            'CONVERSION_SERVICE_PASSWORD': 'dev',
        },
        OSMAXX={
            'download_file_name': '%(date)s-%(excerpt_name)s-%(id)s.%(content_type)s.%(file_extension)s',
            'EXTRACTION_PROCESSING_TIMEOUT_TIMEDELTA': timedelta(hours=24),
            # The email adress of this user will be used to generate the mailto link for users
            # to request access to osmaxx (access_denied page)
            'CONVERSION_SERVICE_URL': 'http://localhost:8901/api/',
            'CONVERSION_SERVICE_USERNAME': 'dev',
            'CONVERSION_SERVICE_PASSWORD': 'dev',
        },
        OSMAXX_FRONTEND_USER_GROUP='osmaxx_frontend_users',

        CACHES={
            'default': {
                'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
                'LOCATION': ''
            }
        },
        MIGRATION_MODULES={
            'sites': 'osmaxx.contrib.sites.migrations',
            'auth': 'osmaxx.contrib.auth.migrations',
            'stored_messages': 'osmaxx.third_party_apps.stored_messages.migrations',
        }
    )


# if any global fixtures are needed, add them below

@pytest.yield_fixture
def requests_mock():
    import requests_mock
    with requests_mock.mock() as m:
        yield m


@pytest.fixture
def user(db, django_user_model, django_username_field):
    """A Django user.

    This uses an existing user with username "user", or creates a new one with
    password "password".
    """
    # Adapted from pytest_django.fixtures.admin_user
    UserModel = django_user_model  # noqa
    username_field = django_username_field
    username = 'user'
    password = 'password'

    try:
        user = UserModel._default_manager.get(**{username_field: 'user'})
    except UserModel.DoesNotExist:
        extra_fields = {}
        if username_field != 'username':
            extra_fields[username_field] = username
        user = UserModel._default_manager.create_user(
            username, '{}@example.com'.format(username), password, **extra_fields)
    return user


@pytest.fixture
def authenticated_client(client, user):
    """
    Client fixture using an authenticated user.

    Since this fixture creates a database object, you must
    mark your test with @pytest.mark.django_db()


    Args:
        client: Default client fixture from pytest-django

    Returns:
        Authenticated Client
    """
    client.login(username='user', password='password')
    client.user = user
    return client


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def authenticated_api_client(api_client, user):
    """
    API-Client fixture using an authenticated user.

    Since this fixture creates a database object, you must
    mark your test with @pytest.mark.django_db()


    Args:
        api_client: api-client fixture

    Returns:
        Authenticated Client
    """
    return authenticated_client(api_client, user)


@pytest.fixture
def persisted_valid_clipping_area():
    from django.contrib.gis.geos import Polygon, MultiPolygon
    from osmaxx.clipping_area.models import ClippingArea
    poly_1 = Polygon(((0, 0), (0, 1), (1, 1), (0, 0)))
    poly_2 = Polygon(((1, 1), (1, 2), (2, 2), (1, 1)))
    multi_polygon = MultiPolygon(poly_1, poly_2)
    persisted_valid_clipping_area = ClippingArea.objects.create(name='test', clipping_multi_polygon=multi_polygon)
    assert persisted_valid_clipping_area.osmosis_polygon_file_string != ''
    assert persisted_valid_clipping_area.osmosis_polygon_file_string is not None
    assert str(persisted_valid_clipping_area) == "test ({})".format(persisted_valid_clipping_area.id)
    return persisted_valid_clipping_area


@pytest.fixture
def authorized_client(authenticated_client):
    from django.contrib.auth.models import Group
    from osmaxx.contrib.auth.frontend_permissions import FRONTEND_USER_GROUP
    authenticated_client.user.groups.add(Group.objects.get(name=FRONTEND_USER_GROUP))
    return authenticated_client


@pytest.fixture
def geos_geometry_can_be_created_from_geojson_string():
    """
    Just a sanity check asserting that GEOSGeometry instances can be created from GeoJSON strings.

    If you get an error here, check your libraries, especially GDAL. (libgdal.so.1)
    """
    from django.contrib.gis.geos import GEOSGeometry
    import json
    geojson_point = dict(type="Point", coordinates=[100.0, 0.0])
    geojson_point_string = json.dumps(geojson_point)
    GEOSGeometry(geojson_point_string)


@pytest.fixture
def area_polyfile_string():
    return ''''none
polygon-1
    7.495679855346679 43.75782881091782
    7.38581657409668 43.75782881091782
    7.38581657409668 43.70833803832912
    7.495679855346679 43.75782881091782
END
END
'''
