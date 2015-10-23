from datetime import timedelta


def pytest_configure():
    from django.conf import settings

    settings.configure(
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
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
            'rest_framework.authtoken',
            'tests',
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
            'high': {
                'HOST': 'localhost',
                'PORT': 6379,
                'DB': 0,
                'PASSWORD': '',
                'DEFAULT_TIMEOUT': 3600,
            },
            'low': {
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
    )
