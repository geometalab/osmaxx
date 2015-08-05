# Osmaxx

Short project name for "<strong>O</strong>pen<strong>S</strong>treet<strong>M</strong>ap <strong>a</strong>rbitrary e<strong>x</strong>cerpt e<strong>x</strong>port".

Cuts out OpenStreetMap data, processes it to geodata and converts it to typical GIS fileformats before being prepared for download.

Website: http://osmaxx.hsr.ch/


## Development

See https://github.com/geometalab/osmaxx-docs for documentations and [/docs/development.md](/docs/development.md) for
more detailed instructions.


## Run it locally on Linux

### Prerequisites

To run this project locally, you need docker and docker-compose installed
(https://docs.docker.com/installation/ubuntulinux/ and https://docs.docker.com/compose/install/).


### Initialization/Docker container bootstrapping

```shell
# For development:
ln -s compose-development.yml docker-compose.yml

# For production:
ln -s compose-production.yml docker-compose.yml
```

To setup all the containers and their dependencies, run

```shell
docker-compose build
```

Then initiate the project defaults by running the following command:

```shell
# For development:
docker-compose run osmaxxwebappdev /bin/bash -c 'python3 manage.py migrate && python3 manage.py createsuperuser'

# For production:
docker-compose run osmaxxwebapp /bin/bash -c 'python3 manage.py migrate && python3 manage.py createsuperuser'
```

Alternative to this command, bootstrap the container and execute the commands inside the container by hand:

```shell
# For development:
docker-compose run osmaxxwebappdev /bin/bash

# For production:
docker-compose run osmaxxwebapp /bin/bash
```

Inside the container:

1. Execute migrations: `$ python3 manage.py migrate`
2. (optional, recommended) setup a superuser: `$ python3 manage.py createsuperuser`


### Running the project

Start the containers using docker compose:

```shell
docker-compose up
```


### Documentation

See Wiki: https://github.com/geometalab/osmaxx/wiki


### Problems & Solutions

#### Leaflet is missing

You forgot to **pull the submodules**


#### ProgrammingError at /login/

```
relation "django_site" does not exist
LINE 1: ..."django_site"."domain", "django_site"."name" FROM "django_si...
```

You forgot to **run the migrations**
