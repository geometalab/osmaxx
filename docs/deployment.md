# Deployment

To deploy to production server:

1. Stop the running containers
  ```shell
  docker exec osmaxx-starter /usr/local/bin/docker-compose stop
  ```

2. Rename the old source and clone the repository master branch without history:

  ```shell
  git clone --depth 1 -b master https://github.com/geometalab/osmaxx.git osmaxx && cd osmaxx
  git submodule init && git submodule update
  ```
  Repository details see [Project repository](git-repository.md).
3. a. Link production configuration for docker-compose, Details see [Docker container bootstrapping](../README.md#initializationdocker-container-bootstrapping).
   b. Edit the `compose-production.yml` file and change/add environment settings for celery and webapp. 
      List of available additional settings (no quotes for strings!):
   
       ```
        - DJANGO_EMAIL_HOST=smtp.example.com   # your smtp server for sending
        - DJANGO_EMAIL_HOST_PASSWORD=password   # the password for the smtp server user
        - DJANGO_EMAIL_HOST_USER=myuser    # the username for the smtp server user
        - DJANGO_EMAIL_PORT=25              # the port used by the smtp server
        - DJANGO_EMAIL_SUBJECT_PREFIX=[My-OSMAXX]  # only used for sending mails with `mail_admins` and `mail_managers` 
        - DJANGO_EMAIL_USE_TLS=false  # set to true to enable (case insensitive)
        - DJANGO_EMAIL_USE_SSL=false  # set to true to enable (case insensitive)
        - DJANGO_EMAIL_TIMEOUT=<Number>   # WARNING: only set this if you really want to have a timeout!
        - DJANGO_EMAIL_SSL_CERTFILET=<path>   # WARNING: only set this if you have a certfile
        - DJANGO_EMAIL_SSL_KEYFILE=<path>     # WARNING: only set this if you have a keyfile
       ```

4. Add target specific environment variables to compose-production.yml
  * If you are using an nginx proxy (jwilder/nginx-proxy), you need to set the environment variable
    `VIRTUAL_HOST=osmaxx.yourdomain.tld`
5. Build the containers. Use docker-compose container instead of native installation:

  a. Create the docker-compose container if not already exists:
    ```shell
    # "up" && "--no-recreate": default arguments used by the systemd service starter
    docker create \
      --name osmaxx-starter
      -v "/path/to/source/repo:/app" \
      -v "/var/run/docker.sock:/var/run/docker.sock" \
      -e "COMPOSE_PROJECT_NAME=osmaxx" \
      "dduportal/docker-compose:1.3.1" up --no-recreate
    ```

  b. Pull images & build osmaxx containers:  
    ```shell
    # pull newest images
    # "--rm" removes the temporary used compose-container
    docker run -v "/path/to/source/repo:/app" -v "/var/run/docker.sock:/var/run/docker.sock" -e "COMPOSE_PROJECT_NAME=osmaxx" --rm "dduportal/docker-compose:1.3.1" pull

    # build own containers
    docker run -v "/path/to/source/repo:/app" -v "/var/run/docker.sock:/var/run/docker.sock" -e "COMPOSE_PROJECT_NAME=osmaxx" --rm "dduportal/docker-compose:1.3.1" build
    ```

6. Run migrations and add create super user, Details see [Docker container bootstrapping](../README.md#initializationdocker-container-bootstrapping).
  For docker-compose container run:

  ```shell
  # database needs to be running before the webapp container
  docker run -v "/path/to/source/repo:/app" -v "/var/run/docker.sock:/var/run/docker.sock" -e "COMPOSE_PROJECT_NAME=osmaxx" --rm "dduportal/docker-compose:1.3.1" up -d database

  # apply migrations
  # "-it" is needed to get an interactive terminal
  # "run --rm" removes the temporary used webapp container
  docker run -v "/path/to/source/repo:/app" -v "/var/run/docker.sock:/var/run/docker.sock" -e "COMPOSE_PROJECT_NAME=osmaxx" -it --rm "dduportal/docker-compose:1.3.1" run --rm webapp /bin/bash -c "python3 manage.py migrate && python3 manage.py createsuperuser"

  # stop running containers
  docker run -v "/path/to/source/repo:/app" -v "/var/run/docker.sock:/var/run/docker.sock" -e "COMPOSE_PROJECT_NAME=osmaxx" --rm "dduportal/docker-compose:1.3.1" stop
  ```
7. Load data container content from old container if there is one, Details see [Useful Docker commands](project-development-environment.md#useful-docker-commands).
8. Load database container content from old container if there is one, Details see [Useful Docker commands](project-development-environment.md#useful-docker-commands).
9. Add a system startup script running `docker-compose up`
  E.g. /etc/systemd/system/osmaxx.service:

  ```shell
  [Unit]
  Description=Start osmaxx application

  [Service]
  ExecStart=/usr/bin/docker start -a osmaxx-starter
  ExecStop=/usr/bin/docker exec osmaxx-starter /usr/local/bin/docker-compose stop --timeout 60
  ExecStop=/usr/bin/docker kill --signal=INT osmaxx-starter
  ExecStop=/usr/bin/docker stop -t 10 osmaxx-starter
  Restart=always

  [Install]
  WantedBy=multi-user.target
  ```
  **important**: osmax-starter container needs to be created before!

  "/usr/bin/docker start -a osmaxx-starter" will use the default arguments configured on create.

1. Enable startup service  
  ```shell
  sudo systemctl enable docker-osmaxx.service
  ```

11. Start the containers
  ```shell
  sudo systemctl start docker-osmaxx.service
  ```

## Deploying a Hotfix

First, stop the systemd restarter:
```shell
sudo systemctl stop docker-osmaxx.service
```

Then, follow the steps until 5a from [Deployment](#Deployment).

Replace step `5b` with:

*5b.*

```shell
docker run -v "/path/to/source/repo:/app" -v "/var/run/docker.sock:/var/run/docker.sock" -e "COMPOSE_PROJECT_NAME=osmaxx" --rm "dduportal/docker-compose:1.3.1" pull celery webapp
 ```

In case you're unsure whether Dockerhub was fast enough to build the images already, rebuild containers `webapp` and `celery`:

```shell
docker run -v "/path/to/source/repo:/app" -v "/var/run/docker.sock:/var/run/docker.sock" -e "COMPOSE_PROJECT_NAME=osmaxx" --rm "dduportal/docker-compose:1.3.1" build celery webapp
```

If your hotfix changes the database, also run the migrations:

```shell
docker run -v "/path/to/source/repo:/app" -v "/var/run/docker.sock:/var/run/docker.sock" -e "COMPOSE_PROJECT_NAME=osmaxx" --rm "dduportal/docker-compose:1.3.1" up -d database
docker run -v "/path/to/source/repo:/app" -v "/var/run/docker.sock:/var/run/docker.sock" -e "COMPOSE_PROJECT_NAME=osmaxx" -it --rm "dduportal/docker-compose:1.3.1" run --rm webapp /bin/bash -c "python3 manage.py migrate"
```

Restart the service:

```shell
sudo systemctl start docker-osmaxx.service
```


## List of django settings configurable through environment variables

These settings are all configurable by setting environment variables.
Each ink points to the description in the Django Documentation, we're using 
1.8 currently.

A general [checklist](https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/) 
is also available.

*Remarks*:

* Bold settings need to be set/changed before deploying.
* Settings with a `*` should not be needing any changes, if deployed with our
  docker-compose files. 
* Settings with a `+` are not defined in our docker-compose file and therefore
  set to the default listed below.
* In the defaults, `undefined` means the setting isn't set at all 

List of settings, the default value is assigned if that particular setting isn't
defined in the environment variables or set to an empty string (e.g
`DJANGO_CSRF_COOKIE_SECURE=`):
  
* **DJANGO_SECRET_KEY**: `None`, [SECRET_KEY](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-SECRET_KEY)
* **DJANGO_EMAIL_BACKEND**: `'django.core.mail.backends.smtp.EmailBackend'`, [EMAIL_BACKEND](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-EMAIL_BACKEND)
* **DJANGO_EMAIL_HOST**: `'localhost'`, [EMAIL_HOST](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-EMAIL_HOST)
* **DJANGO_EMAIL_HOST_PASSWORD**: `''`, [EMAIL_HOST_PASSWORD](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-EMAIL_HOST_PASSWORD)
* **DJANGO_EMAIL_HOST_USER**: `''`, [EMAIL_HOST_USER](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-EMAIL_HOST_USER)
* **DJANGO_EMAIL_PORT**: `25`, [EMAIL_PORT](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-EMAIL_PORT)
* **DJANGO_EMAIL_SUBJECT_PREFIX**: `'[Django] '`, [EMAIL_SUBJECT_PREFIX](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-EMAIL_SUBJECT_PREFIX)
* **DJANGO_EMAIL_USE_TLS**: `False`, [EMAIL_USE_TLS](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-EMAIL_USE_TLS)
* **DJANGO_EMAIL_USE_SSL**: `False`, [EMAIL_USE_SSL](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-EMAIL_USE_SSL)
* **DJANGO_EMAIL_TIMEOUT**: `None`, [EMAIL_TIMEOUT](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-EMAIL_TIMEOUT)
* **DJANGO_EMAIL_SSL_CERTFILET**: `None`, [EMAIL_SSL_CERTFILE](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-EMAIL_SSL_CERTFILE)
* **DJANGO_EMAIL_SSL_KEYFILE**: `None`, [EMAIL_SSL_KEYFILE](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-EMAIL_SSL_KEYFILE)
* **DJANGO_DEFAULT_FROM_EMAIL**: `'webmaster@localhost'`, [DEFAULT_FROM_EMAIL](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-DEFAULT_FROM_EMAIL)
* **DJANGO_SERVER_EMAIL**: `'root@localhost'`, [SERVER_EMAIL](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-SERVER_EMAIL)
* **DJANGO_EMAIL_FILE_PATH**: `None`, [EMAIL_FILE_PATH](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-EMAIL_FILE_PATH)
* DJANGO_STATIC_ROOT`*`: `str(ROOT_DIR('..', 'static'))`, [STATIC_ROOT](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-STATIC_ROOT)
* DJANGO_MEDIA_ROOT`*`: `str(ROOT_DIR('..', 'media'))`, [MEDIA_ROOT](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-MEDIA_ROOT)
* DJANGO_PRIVATE_MEDIA_ROOT`*`: `str(ROOT_DIR.path('..', 'private_media'))`, is an Osmaxx specific setting.
* DJANGO_RESULT_MEDIA_ROOT`*`: `str(ROOT_DIR.path('..', 'results_media'))`, is an Osmaxx specific setting.
* DJANGO_CELERY_BROKER_URL`*`: `'amqp://guest:guest@localhost:5672//'`, [BROKER_URL](http://docs.celeryproject.org/en/latest/configuration.html#broker-url)
  Broker URL for the celery process
* **DJANGO_ALLOWED_HOSTS**: `[]`, [ALLOWED_HOSTS](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-ALLOWED_HOSTS)
* DJANGO_X_FRAME_OPTIONS`+`: `'SAMEORIGIN'`, [X_FRAME_OPTIONS](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-X_FRAME_OPTIONS)
* DJANGO_SECURE_BROWSER_XSS_FILTER`*`: `False`, [SECURE_BROWSER_XSS_FILTER](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-SECURE_BROWSER_XSS_FILTER)
* DJANGO_SECURE_CONTENT_TYPE_NOSNIFF`*`: `False`, [SECURE_CONTENT_TYPE_NOSNIFF](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-SECURE_CONTENT_TYPE_NOSNIFF)
* DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS`+`: `False`, [SECURE_HSTS_INCLUDE_SUBDOMAINS](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-SECURE_HSTS_INCLUDE_SUBDOMAINS)
* DJANGO_SECURE_HSTS_SECONDS`+`: `0`, [SECURE_HSTS_SECONDS](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-SECURE_HSTS_SECONDS)
* DJANGO_SECURE_PROXY_SSL_HEADER`+`: `None`, [SECURE_PROXY_SSL_HEADER](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-SECURE_PROXY_SSL_HEADER)
* DJANGO_SECURE_REDIRECT_EXEMPT`+`: `[]`, [SECURE_REDIRECT_EXEMPT](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-SECURE_REDIRECT_EXEMPT)
* DJANGO_SECURE_SSL_HOST`+`: `None`, [SECURE_SSL_HOST](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-SECURE_SSL_HOST)
* DJANGO_SECURE_SSL_REDIRECT`+`: `False`, [SECURE_SSL_REDIRECT](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-SECURE_SSL_REDIRECT)
* **DJANGO_CSRF_COOKIE_SECURE**: `False`, [CSRF_COOKIE_SECURE](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-CSRF_COOKIE_SECURE)
* DJANGO_CSRF_COOKIE_HTTPONLY`+`: `False`, [CSRF_COOKIE_HTTPONLY](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-CSRF_COOKIE_HTTPONLY)
* DJANGO_CSRF_COOKIE_DOMAIN`+`: `None`, [CSRF_COOKIE_DOMAIN](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-CSRF_COOKIE_DOMAIN)
* DJANGO_CSRF_COOKIE_NAME`+`: `'csrftoken'`, [CSRF_COOKIE_NAME](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-CSRF_COOKIE_NAME)
* DJANGO_CSRF_COOKIE_PATH`+`: `'/'`, [CSRF_COOKIE_PATH](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-CSRF_COOKIE_PATH)
* DJANGO_CSRF_FAILURE_VIEW`+`: `'django.views.csrf.csrf_failure'`, [CSRF_FAILURE_VIEW](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-CSRF_FAILURE_VIEW)
* DJANGO_SESSION_CACHE_ALIAS`+`: `'default'`, [SESSION_CACHE_ALIAS](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-SESSION_CACHE_ALIAS)
* DJANGO_SESSION_COOKIE_AGE`+`: `timedelta(weeks=2).total_seconds()`, [SESSION_COOKIE_AGE](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-SESSION_COOKIE_AGE)
* DJANGO_SESSION_COOKIE_DOMAIN`+`: `None`, [SESSION_COOKIE_DOMAIN](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-SESSION_COOKIE_DOMAIN)
* DJANGO_SESSION_COOKIE_HTTPONLY`+`: `True`, [SESSION_COOKIE_HTTPONLY](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-SESSION_COOKIE_HTTPONLY)
* DJANGO_SESSION_COOKIE_NAME`+`: `'sessionid'`, [SESSION_COOKIE_NAME](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-SESSION_COOKIE_NAME)
* DJANGO_SESSION_COOKIE_PATH`+`: `'/'`, [SESSION_COOKIE_PATH](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-SESSION_COOKIE_PATH)
* **DJANGO_SESSION_COOKIE_SECURE**: `False`, [SESSION_COOKIE_SECURE](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-SESSION_COOKIE_SECURE)
* DJANGO_SESSION_ENGINE`+`: `'django.contrib.sessions.backends.db'`, [SESSION_ENGINE](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-SESSION_ENGINE)
* DJANGO_SESSION_EXPIRE_AT_BROWSER_CLOSE`+`: `False`, [SESSION_EXPIRE_AT_BROWSER_CLOSE](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-SESSION_EXPIRE_AT_BROWSER_CLOSE)
* DJANGO_SESSION_FILE_PATH`+`: `None`, [SESSION_FILE_PATH](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-SESSION_FILE_PATH)
* DJANGO_SESSION_SAVE_EVERY_REQUEST`+`: `False`, [SESSION_SAVE_EVERY_REQUEST](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-SESSION_SAVE_EVERY_REQUEST)
* DJANGO_SESSION_SERIALIZER`+`: `'django.contrib.sessions.serializers.JSONSerializer'`, [SESSION_SERIALIZER](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-SESSION_SERIALIZER)
* DJANGO_LOG_LEVEL`*`: `DEBUG`, [logging handlers](https://docs.djangoproject.com/en/1.8/topics/logging/#loggers)
* **DJANGO_DEBUG**: `False`, [DEBUG](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-DEBUG)

## Django unrelated environment variables

Defaults refer to the setting in compose-common.yml.

Special application settings:

* APP_HOST`*`: which host/interface it is listening on (where `0.0.0.0` stands for `all interfaces`)
* APP_PORT`*`: which port the application listens on
* DJANGO_DATABASE_URL: [DATABASES](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-DATABASES)
  setting through [django-environ](https://django-environ.readthedocs.org/en/latest/#supported-types),
  using [dj-database-url](https://github.com/kennethreitz/dj-database-url#usage)

Special docker and python related environment settings:

* PYTHONUNBUFFERED: `non-empty-string`, [no buffering](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONUNBUFFERED), better for logging in docker
* PYTHONIOENCODING: `utf-8`, better logging in docker with defined utf-8 strings. [PYTHONIOENCODING](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONIOENCODING)
* PYTHONHASHSEED: `random`, [security enhancement](https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/#python-options)
