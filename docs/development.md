# Development

We do not recommend to run the application local on your machine but it's possible. We recommend to use the development docker containers.

**NOTE**: to run it locally (no docker), you might want to copy the .env-dist
to .env and adapt the lines there.


## Git repository

For developers have write access to this repository:

1. Clone this GitHub repository to your local machine and change into the local repo
	```shell
	git clone git@github.com:geometalab/osmaxx.git osmaxx && cd osmaxx
	```
	You can specify the name of the remote origin by adding param -o. Example: `-o 'gitHub'`

2. Enable [git-flow](https://github.com/nvie/gitflow) for the local repo
	```shell
	git flow init -d
	```

	(This project uses git-flow's default branch names and branch name prefixes, which `-d` automatically accepts.)

	You should now be on the `develop` branch. Otherwise checkout the development branch: `git checkout development`.
3. Clone the third party repositories we use through [git submodules](http://www.git-scm.com/book/en/v2/Git-Tools-Submodules)
	```shell
	git submodule init && git submodule update
	```


### Contribute

1. Create a feature branch for your contribution
	```shell
	git flow feature start 'my-awesome-feature#gitHubIssueNumber'
	```

2. Code and commit as usual
3. Run flake8, checks and tests
	```shell
	./test.sh
	```

3. Once you're finished, push the feature branch back to this GitHub repo
	```shell
	git flow feature publish
	```

	(Do **not** use `git flow feature finish`, as we use pull requests for review purposes.)

4. Create a pull request against branch `develop`. Link the issue, inform the reviewers about the checks you did and add review tasks as subtasks (see below), e.g:
	```markdown
	Implementation of feature #123 (Merge will close #123 ).

	* locales **NOT** compiled -> do this on release (prevent huge locale diffs in changes)
	* ran flake8
	* ran check
	* ran test
	* tested views by hand:
	  * /orders/new [get/post]
	  * /orders/{id}

	To be reviewed by:
	- [ ] @some-developer
	- [ ] @another-developer
	```


### Release

* Compile locales
* Run all tests
* Test development and production containers
* Update documentation
	* Readme
	* Wiki


## Project Development Environment (Docker)

### Local prerequisites

Docker and docker-compose is required to be installed.

For committing and using the pre-commit hook (which really should be used) flake8 needs to be installed on
the local system/machine.

For Ubuntu and Debian this is:

```shell
sudo apt-get install python3-flake8
```

Then the pre-commit hook can be linked to the hooks.

```hell
$ cd <osmaxx-repo-root>
$ ln -s ../../hooks/pre-commit .git/hooks/pre-commit
```


### Using the project docker setup

A docker-compose setup is provided as part of this project's repository. Ensure to have docker installed
and setup the containers properly, as described in the README.


### Running commands

The general way of running any command inside a docker container:

```shell
docker-compose run <container> <command>
```

Examples:

Execute a shell in the webapp:
```shell
docker-compose run osmaxxwebappdev /bin/bash
```


### Run tests
```shell
./test.sh
```

To run the application tests only, see [Commonly used commands while developing / Run tests](#run-tests).


### Access the application

[http://localhost:8000](http://localhost:8000)

or add

```txt
127.0.0.1	osmaxx.dev
```

to your `/etc/hosts` file and access by

[http://osmaxx.dev:8000](http://osmaxx.dev:8000)


### Reset the box

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


## Commonly used commands while developing

### Update persistence

#### Update migration information

```shell
docker-compose run osmaxxwebappdev /bin/bash -c 'python3 manage.py makemigrations'
```

#### Run migrations on database
```shell
docker-compose run osmaxxwebapp /bin/bash -c 'python3 manage.py migrate'
```

### Run tests
```shell
docker-compose run osmaxxwebappdev /bin/bash -c 'python3 manage.py test'
```


### Use backend

#### Create superuser

```shell
docker-compose run webapp /bin/bash -c 'python3 manage.py createsuperuser'
```

### Update locales
Please update locales only on release. Otherwise you will get huge diffs in feature pull requests.

```shell
docker-compose run webapp /bin/bash -c 'python3 manage.py makemessages -a'
```


### Deployment
