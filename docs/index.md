<div class="badges">
    <a href="http://travis-ci.org/geometalab/osmaxx-conversion-service">
        <img src="https://travis-ci.org/geometalab/osmaxx-conversion-service-api.svg?branch=master">
    </a>
    <a href="https://pypi.python.org/pypi/osmaxx-conversion-service">
        <img src="https://img.shields.io/pypi/v/osmaxx-conversion-service-rest-api.svg">
    </a>
</div>

---

# osmaxx-conversion-service-rest-api

conversion service API Frontend for Osmaxx

---

## Overview

conversion service API Frontend for Osmaxx

## Requirements

* Python (3.4)
* postgres-server-headers (dev) for psycopg2

For required Python 3 packages, see `requirements.txt`.

## Installation

### local development

```bash
docker-compose stop -t 0 &&\
 docker-compose build &&\
 docker-compose run --rm -e osm_planet_mirror=http://download.geofabrik.de/europe/ -e osm_planet_path_relative_to_mirror=switzerland-latest.osm.pbf osmdata &&\
 docker-compose run --rm osmdata mv /var/data/osm-planet/switzerland-latest.osm.pbf /var/data/osm-planet/planet-latest.osm.pbf &&\
 docker-compose up -d worker &&\
 docker-compose run --rm api ./conversion_service/manage.py createsuperuser &&\
 docker-compose up api
```

### on the server

```bash
docker-compose build &&\
 docker-compose run --rm osmdata &&\
 docker-compose up -d worker &&\
 docker-compose up api
```

and to create an initial user:

```bash
docker-compose run --rm api ./conversion_service/manage.py createsuperuser
```

## Example

TODO: Write example.

## Linting

Using the instruction below for testing, the flake8 tool is also run.

For more comprehensive output, you can use prospector:

```bash
prospector --with-tool vulture --with-tool pyroma
```

Information about its options and usage can be found at the 
[prospector documentation](http://prospector.readthedocs.org/en/master/usage.html)

## Testing

For all tests, a redis-server instance is required.

The most simple way is to run an instance using docker (in a separate bash terminal):

```bash
docker run -p 6379:6379 --rm --name redis-local redis
```

Install testing requirements.

```bash
$ pip install -r requirements.txt
```

Run with runtests.

```bash
$ ./runtests.py
```

You can also use the excellent [tox](http://tox.readthedocs.org/en/latest/) testing tool to run the tests against all supported versions of Python and Django. Install tox globally, and then simply run:

```bash
$ tox
```

## Documentation

To build the documentation, you'll need to install `mkdocs`.

```bash
$ pip install mkdocs
```

To preview the documentation:

```bash
$ mkdocs serve
Running at: http://127.0.0.1:8000/
```

To build the documentation:

```bash
$ mkdocs build
```
