# Osmaxx

Short project name for "<strong>O</strong>pen<strong>S</strong>treet<strong>M</strong>ap <strong>a</strong>rbitrary e<strong>x</strong>cerpt e<strong>x</strong>port".

Cuts out OpenStreetMap data, processes it to geodata and converts it to typical GIS fileformats before being prepared for download.

Website: http://osmaxx.hsr.ch/


## Development

* [Project Repository (Git)](/docs/git-repository.md)
* [Project Development Environment (Docker)](/docs/project-development-environment.md)
* [Commonly used commands for development](/docs/useful-commands.md)
* [Deployment](/docs/deployment.md)
* [Testing](/docs/testing.md)

We do not recommend to run the application local on your machine but it's possible. We recommend to use the development docker containers.

## Run it locally on Linux (Development)

### Prerequisites

To run this project locally, you need docker and docker-compose installed
(https://docs.docker.com/installation/ubuntulinux/ and https://docs.docker.com/compose/install/).


### Initialization

```shell
# For development:
ln -s compose-development.yml docker-compose.yml
```

### Docker container bootstrapping

Take a look at the script ```setup.development.sh```.
These script will setup the container forest, run migrations and create a superuser (interactive).

To setup all the containers and their dependencies by hand, run

```shell
docker-compose build
```

Then initiate the project defaults by running the following command:

```shell
docker-compose run webappdev /bin/bash -c './manage.py createsuperuser'
```

Alternative to this command, bootstrap the container and execute the commands inside the container by hand:

```shell
docker-compose run webappdev /bin/bash
```

Inside the container:

1. (optional, recommended) setup a superuser: `$ ./manage.py createsuperuser`


### Running the project

Start the containers using docker compose:

```shell
docker-compose up
```

Unsure which version is running?

Go to `localhost:8000/version/`.

### Testing

Can be found under [Testing](/docs/testing.md).


### Documentation

See Wiki: https://github.com/geometalab/osmaxx/wiki


### Problems & Solutions

#### ProgrammingError at /login/

```
relation "django_site" does not exist
LINE 1: ..."django_site"."domain", "django_site"."name" FROM "django_si...
```

You forgot to **run the migrations**


#### Tests failed, but worked before with no apparent change

Do not run `docker-compose build --no-cache`. Use `docker-compose rm -f && docker-compose build`, or
if you really want to start clean, remove all docker containers

`docker rm -f $(docker ps -q)`

and remove all images

`docker rmi -f $(docker images -q)`

*WARNING*: This removes all containers/images on the machine.
