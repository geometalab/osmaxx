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
 docker-compose run --rm osmdata cp /var/data/osm-planet/switzerland-latest.osm.pbf /var/data/osm-planet/planet-latest.osm.pbf &&\
 docker-compose up -d worker &&\
 docker-compose run --rm api ./osmaxx/manage.py createsuperuser &&\
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
docker-compose run --rm api ./osmaxx/manage.py createsuperuser
```

## Example

```python
import requests
```

### Login

```python
url = 'http://localhost:9000/api/token-auth/?format=json'
headers = {'Content-Type': 'application/json; charset=UTF-8'}
data = {'username':'osmaxx', 'password':'osmaxx'}

token_request = requests.post(url, data=json.dumps(data), headers=headers)
token = token_request.json()['token']
```


### Create conversion job

```python
url = 'http://localhost:9000/api/jobs/'
headers = {'Content-Type': 'application/json; charset=UTF-8', 'Authorization': 'JWT ' + token}
data = {
    "callback_url": "http://example.com",
    "gis_formats": ["fgdb", "spatialite"],
    "gis_option": {"coordinate_reference_system": "WGS_84","detail_level": 1},
    "extent": {
        "west": 29.525547623634335,
        "south": 40.77546776498174,
        "east": 29.528980851173397,
        "north": 40.77739734768811,
        "polyfile": None
    }
}

conversion_request = requests.post(url, data=json.dumps(data), headers=headers)
conversion = conversion_request.json()
```

### Get job status

```python
url = 'http://localhost:9000/api/conversion_result/8b5285ad-e785-4812-82d2-376a61ebd9d3/'
headers = {'Content-Type': 'application/json; charset=UTF-8', 'Authorization': 'JWT ' + token}

response = requests.get(url, headers=self.headers)
status = response.json()
job_status = status['status']
```

### Download result files

```python
if job_status and job_status['status'] == 'done' and job_status['progress'] == 'successful':
    for download_file in job_status['gis_formats']:
        if download_file['progress'] == 'successful':
            result_response = requests.get(download_file['result_url'], headers=self.headers)
            file_name = ...
            file = storage.save(file_name, ContentFile(result_response.content))
```


## Linting

Using the instruction below for testing, the flake8 tool is also run.

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
