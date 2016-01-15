# Development

# Git repository

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
	    
	**and** create a pull request against branch `develop`. (Do **not** use `git flow feature finish`, as we use pull requests for review purposes.)

# Project Development Environment (Docker)

A docker-compose setup is provided as part of this project's repository.

## Local prerequisites

For committing and using the pre-commit hook (which really should be used) flake8 needs to be installed on
the local system/machine.

For Ubuntu and Debian this is:

`sudo apt-get install python3-flake8`

Then the pre-commit hook can be linked to the hooks.

```
$ cd <osmaxx-repo-root>
$ ln -s ../../hooks/pre-commit .git/hooks/pre-commit
```

### Reset the box

```shell
docker-compose build
```

Is usually enough, since it builds the changed parts only. If it is not enough, first use

```shell
docker-compose stop
docker-compose rm # and say yes
docker-compose build
```

If you really want to go and have a coffee, you might use the following:

```shell
docker-compose build --no-cache
```


### do something in a box

```shell
docker-compose run <container> <command>
```

ie.

```shell
docker-compose run webapp bash
```

## Development

### Update persistence

#### Update migration information

```shell
docker-compose run webapp python3 manage.py makemigrations
```

#### Run migrations on database
```shell
docker-compose run webapp python3 manage.py migrate
```


### Use backend

#### Create superuser

```shell
docker-compose run webapp python3 manage.py createsuperuser
```

### Update locales

```shell
docker-compose run webapp python3 manage.py makemessages -a
```


### Backup & restore the database
```shell
# backup
docker save osmaxx_database > database_backup_file.docker
# restore
docker load < database_backup_file.docker
```


### Deployment

#### Package release

TODO: simplify the release process.

```shell
cd toDirectoryContainingOsmaxxRepo
zip -r osmaxx-0.1.zip osmaxx -x *.git* -x *.od* -x *.gitignore* -x *.gitmodules* -x *developmentEnvironment/* -x *data/* -x *.idea* -x *test_db.sqlite* -x *__pycache__*
```
