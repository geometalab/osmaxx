# Development

**NOTE**: to run it locally (no docker), you might want to copy the .env-dist
to .env and adapt the lines there.

## Git repository

For developers with write access to this repository:

1. Clone this GitHub repository to your local machine and change into the local repo
	```shell
    git clone git@github.com:geometalab/osmaxx.git osmaxx && cd osmaxx
    ```
    You can specify the name of the remote origin by adding param -o. Example: -o 'gitHub' 
    
2. Enable [git-flow](https://github.com/nvie/gitflow) for the local repo

	    git flow init -d
	    
	(This project uses git-flow's default branch names and branch name prefixes, which `-d` automatically accepts.)
3. (You should now be on the `develop` branch.)

	Clone the third party repositories we use through [git submodules](http://www.git-scm.com/book/en/v2/Git-Tools-Submodules)

	    git submodule init
	    git submodule update
	    
4. Create a feature branch for your contribution

	    git flow feature start my-awesome-contribution
	    
5. Make your commits as usual
6. Once you're finished, push the feature branch back to this GitHub repo

	    git flow feature publish
	    
	**and** create a pull request against branch `develop`. 
	(Do **not** use `git flow feature finish`, as we use pull requests for review purposes.)

## Project Development Environment (Docker)

### Local prerequisites

Docker and docker-compose is required to be installed.

For committing and using the pre-commit hook (which really should be used) flake8 needs to be installed on
the local system/machine.

For Ubuntu and Debian this is:

`sudo apt-get install python3-flake8`

Then the pre-commit hook can be linked to the hooks.

```
$ cd <osmaxx-repo-root>
$ ln -s ../../hooks/pre-commit .git/hooks/pre-commit
```

### Using the project docker setup

A docker-compose setup is provided as part of this project's repository. Ensure to have docker installed
and setup the containers properly, as described in the README.


**IMPORTANT**: there are some issues with permissions on the docker container. Please ensure
you run the following, before starting with the setup:

```shell
$ mkdir -p docker_mounts/media
$ mkdir -p docker_mounts/static
$ mkdir -p docker_mounts/private_media
$ chown -R 1000:1000 docker_mounts
```

### Running commands

The general way of running any command inside a docker container:

```shell
docker-compose run <container> <command>
```

Examples:

Execute a shell in the webapp:

```shell
docker-compose run webapp /bin/bash
```
Run tests:

`docker-compose run webapp /bin/bash -c 'python3 manage.py test'`


### Access the application

[http://localhost:8000](http://localhost:8000)

or add 

```127.0.0.1	osmaxx.dev```

to your /etc/hosts file and access by

[http://osmaxx.dev:8000](http://osmaxx.dev:8000)



### Reset the box

Normally, just stopping the containers, removing them and updating them is enough:

```shell
docker-compose kill  # shutdown all containers forcefully
docker-compose rm  # answer yes, so the available containers are destroyed
docker-compose build
docker-compose run webapp /bin/bash
# Inside the container:
python3 manage.py migrate
python3 manage.py createsuperuser
```

If it should be rebuilt from scratch, destroy the boxes and start over. 
Replace the step `docker-compose build` above with `docker-compose build --no-cache`.
**NOTICE**: This might not be what you want; you rebuild single images using 
`docker-compose build --no-cache <imagename>`, so for example, rebuilding the webapp would be
`docker-compose build --no-cache webapp`.

## Useful Docker commands

Save docker image to file:
```shell
docker save osmaxx_database > /tmp/osmaxx-database-alpha1.docker-img.tar
docker save osmaxx_webapp > /tmp/osmaxx-webapp-alpha1.docker-img.tar
```

Load docker image from file:
```shell
docker load < /tmp/osmaxx-database-alpha1.docker-img.tar
docker load < /tmp/osmaxx-database-alpha1.docker-img.tar
```

## Commonly used commands while developing

### Update persistence

#### Update migration information

```shell
docker-compose run webapp /bin/bash -c 'python3 manage.py makemigrations'
```

#### Run migrations on database
```shell
docker-compose run webapp /bin/bash -c 'python3 manage.py migrate'
```


### Use backend

#### Create superuser

```shell
docker-compose run webapp /bin/bash -c 'python3 manage.py createsuperuser'
```

### Update locales

```shell
docker-compose run webapp /bin/bash -c 'python3 manage.py makemessages -a'
```


### Backup & restore the database
```shell
# backup
docker save osmaxx_database > database_backup_file.docker
# restore
docker load < database_backup_file.docker
```


### Feature delivery for review (Pull request)

Before pushing a new feature, please check the following issues and note the done checks:

* compile locales if necessary
* run manage.py check
* run manage.py test
* run flake8
* test views and workflows by hand (GET & POST)


### Deployment

#### Package release

TODO: simplify the release process.

```shell
cd toDirectoryContainingOsmaxxRepo
zip -r osmaxx-0.1.zip osmaxx -x *.git* -x *.od* -x *.gitignore* -x *.gitmodules* -x *developmentEnvironment/* -x *data/* -x *.idea* -x *test_db.sqlite* -x *__pycache__*
```
