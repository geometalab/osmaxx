# Osmaxx

Short project name for "<strong>O</strong>pen<strong>S</strong>treet<strong>M</strong>ap <strong>a</strong>rbitrary e<strong>x</strong>cerpt e<strong>x</strong>port".

Cuts out OpenStreetMap data, processes it to geodata and converts it to typical GIS fileformats before being prepared for download. 

Website: http://osmaxx.hsr.ch/

## Development

See https://github.com/geometalab/osmaxx-docs for documentations and `/docs/development.md` for 
more detailed instructions.

## Run it locally on Linux

### Prerequisites

To run this project locally, you need docker and docker-compose installed 
(https://docs.docker.com/installation/ubuntulinux/ and https://docs.docker.com/compose/install/).

### Initialization/Docker container bootstrapping

```shell
ln -s compose-development.yml docker-compose.yml
```

To setup all the containers and their dependencies, run

`docker-compose build`

Then initiate the project defaults:

`docker-compose run webapp /bin/bash`

Inside the container:

1. Install dependencies: `$ pip3 install -r requirements/local.txt`
2. Execute migrations: `$ python3 manage.py migrate`
3. (optional, recommended) setup a superuser: `$ python3 manage.py createsuperuser`

### Running the project

Start the containers using docker compose:

`docker-compose up`

# Documentation

See Wiki: https://github.com/geometalab/osmaxx/wiki
