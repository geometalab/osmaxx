# Development

## Setup project

### Required Variables

copy .env-dist to .env and fill the secret keys
```bash
SOCIAL_AUTH_OPENSTREETMAP_KEY=
SOCIAL_AUTH_OPENSTREETMAP_SECRET=
```

With values from the [openstreetmap.org](https://www.openstreetmap.org) (`https://www.openstreetmap.org/user/<user>/oauth_clients/` where user is your username) application settings. (Calback URL is `http://localhost:8080/`)

### Startup and Running

Uses docker for all steps, and except the last one is quite common to be using nowadays.

* build: `docker compose build --pull`
* start: `docker compose up --build` (`--build` can be left out, if no new build is to be expected)
* Create a Superuser (to login into backend at http://localhost:8080/admin):
    ```bash
    docker-compose run --rm frontend /bin/bash -c './manage.py createsuperuser'
    ```

## Developing

### Database Migrations

Whenever models are changed, run (and check into git) the changes:

```bash
docker compose run --rm frontend bash -c 'poetry run ./manage.py makemigrations'
```

## Testing

### Run Tests

```bash
# stop running processes
docker compose stop
docker compose up -d frontenddatabase
docker compose run --rm frontend bash -c 'DJANGO_SETTINGS_MODULE= poetry run pytest tests/'
docker compose stop
```

### Prod images test

Testing things locally (ie. letting the prod builds run).

Manual Testing for release:

```bash
docker compose -f docker/docker-compose.prod-test.yml build
docker compose -f docker/docker-compose.prod-test.yml up --build
```

Navigate to localhost:8181 to see, if it is booting up.
If it does, try a small excerpt, and if that works,
make a new release.
This is an area where automated test might
improve the situation of manually testing.

After this, clean up:

```bash
docker compose -f docker/docker-compose.prod-test.yml down -v
```

## Releasing

Update the version, and release new docker images.

Version bumps should be made in the pyproject file at [`osmaxx/pyproject.toml`](../../osmaxx/pyproject.toml).

FIXME: Create a release script, and/or automate the process.

## Update database schema

### Update migration information

```shell
docker-compose run frontend bash -c 'poetry run ./manage.py makemigrations'
```

### Run migrations on database
```shell
docker-compose run frontend bash -c 'poetry run ./manage.py migrate'
```

## Use backend

### Create superuser

```shell
docker-compose run frontend bash -c 'poetry run ./manage.py createsuperuser'
```

### Update locales
Please update locales only on release. Otherwise you will get huge diffs in feature pull requests.

```shell
docker-compose run frontend bash -c 'poetry run ./manage.py makemessages -a'
```
