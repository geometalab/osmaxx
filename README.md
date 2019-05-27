[![Build Status](https://travis-ci.org/geometalab/osmaxx.svg?branch=master)](https://travis-ci.org/geometalab/osmaxx) ([branch `master`](https://github.com/geometalab/osmaxx/tree/master))

Django-based Web Frontend for **osmaxx**.

## Development

[![Build Status](https://travis-ci.org/geometalab/osmaxx.svg?branch=develop)](https://travis-ci.org/geometalab/osmaxx) ([branch `develop`](https://github.com/geometalab/osmaxx/tree/develop))

* [Project Repository (Git)](/docs/development/git-repository.md)
* [Project Development Environment (Docker)](/docs/development/project-development-environment.md)
* [Commonly used commands for development](/docs/development/useful-commands.md)
* [Testing](/docs/development/testing.md)

We do not recommend to run the application local on your machine but it's possible. We recommend to use the development docker containers.

## Run it locally on Linux (Development)

### Prerequisites

To run this project locally, you need [sufficiently recent versions](/docs/development/project-development-environment.md#local-prerequisites) of [docker](/docs/development/project-development-environment.md#dependency_docker) and [docker-compose](/docs/development/project-development-environment.md#dependency_docker-compose) installed.


### Initialization

#### Development

Simply run

```shell
make local_dev_env
```

to set up `*.env` files suitable for local use of our docker-compose files. **Do not use this for production!** It will make use of insecure and hard coded passwords.

#### Production

Copy the environment folder `compose-env-dist` to `compose-env` and adapt the latter's content.

```shell
cp -r compose-env-dist compose-env
# Then, edit compose-env/*.env
```

### Docker container bootstrapping


#### Development 

For the rest of the readme, if in development:

* set `DEPLOY_VERSION` to `local` (`export DEPLOY_VERSION=local`)
* use `docker-compose -f docker-compose.yml -f docker-compose-dev.yml`

or source the helper script `source activate_local_development`. This enables to use `docker-compose` without
all the `-f` options and without needing to specify `DEPLOY_VERSION`.

To setup all the containers and their dependencies by hand, run

```shell
docker-compose build
```

#### Production

In production, you should be setting `DEPLOY_VERSION=xxx` before running any of the commands below, where `xxx` is
the version you'd like to deploy.


#### Generic

The rest of the documentation can be followed independently if on production or on development. 

Update the containers

```shell
docker-compose pull
```

Then initiate the project defaults by running the following command:

```shell
docker-compose run frontend /bin/bash -c './manage.py createsuperuser'
```

Alternative to this command, bootstrap the container and execute the commands inside the container by hand:

```shell
docker-compose run frontend /bin/bash
```

Inside the container:

1. (optional, recommended) setup a superuser: `$ ./manage.py createsuperuser`


### Running the project

Start the containers using docker compose:

```shell
docker-compose up
```

Unsure which version is running?

Go to `<your_ip>:8889/version/`.

where `<your_ip>` is your public IP.

### Testing

Can be found under [Testing](/docs/development/testing.md).


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

*WARNING*: This removes all containers/images on the machine and is
discouraged in production.
