# Project Development Environment (Docker)

## Local prerequisites

Docker and docker-compose is required to be installed.

For committing and using the pre-commit hook (which really should be used) flake8 needs to be installed on
the local system/machine.

For Ubuntu and Debian this is:

```shell
sudo apt-get install python3-flake8
```

Then the pre-commit hook can be linked to the hooks.

```shell
$ cd <osmaxx-repo-root>
$ ln -s ../../hooks/pre-commit .git/hooks/pre-commit
```


## Using the project docker setup

A docker-compose setup is provided as part of this project's repository. Ensure to have docker installed
and setup the containers properly, as described in the README.


## Running commands

The general way of running any command inside a docker container:

```shell
docker-compose run <container> <command>
```

Examples:

Execute a shell in the webapp:
```shell
docker-compose run osmaxxwebappdev /bin/bash
```


## Run tests
```shell
./test.sh
```

To run the application tests only, see [Commonly used commands while developing / Run tests](useful-dommands.md#run-tests).


## Access the application

[http://localhost:8000](http://localhost:8000)

or add

```txt
127.0.0.1	osmaxx.dev
```

to your `/etc/hosts` file and access by

[http://osmaxx.dev:8000](http://osmaxx.dev:8000)


## Reset the box

Normally, just stopping the containers, removing them and updating them is enough:

```shell
docker-compose stop # shutdown all containers
# to force shutdown: docker-compose kill
docker-compose rm -f
docker-compose build

# run migrations and create super user, commands see in README
```


If it should be rebuilt from scratch, destroy the boxes and start over.
Replace the step `docker-compose build` above with `docker-compose build --no-cache`.

**NOTICE**: This might not be what you want; you rebuild single images using
`docker-compose build --no-cache <imagename>`, so for example, rebuilding the webapp would be
`docker-compose build --no-cache osmaxxwebappdev`.


## Useful Docker commands

Save docker image to file:
```shell
docker save osmaxx_osmaxxdatabase > /tmp/osmaxx-database-alpha1.docker-img.tar
docker save osmaxx_osmaxxwebapp > /tmp/osmaxx-webapp-alpha1.docker-img.tar
```

Load docker image from file:
```shell
docker load < /tmp/osmaxx-database-alpha1.docker-img.tar
docker load < /tmp/osmaxx-database-alpha1.docker-img.tar
```
