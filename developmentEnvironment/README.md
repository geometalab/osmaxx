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

# Project Development Environment (Vagrant Box)

A vagrant box is provided as part of this project's repository.

## Features

* Ubuntu 14.04	http://www.ubuntu.com/download/server
* Python3 / pip-3
* Django 		https://docs.djangoproject.com/en/1.7/
* Postgresql 	http://wiki.ubuntuusers.de/PostgreSQL
* OSM Tools
* Postgis



## Setup

1. Download and install newest Version of Virtualbox: https://www.virtualbox.org/wiki/Downloads
	* Ubuntu: Do not use the older version from sources because of incompatibility with new Vagrant
2. Download and install newest Version of Vagrant: https://www.vagrantup.com/downloads.html
	* Ubuntu: Do not use the older version from sources, because of different syntax of vagrant files for older versions
3. Navigate to "developmentEnvironment", run "vagrant up" to start bring up the machine
4. On first start up, Vagrant will download the box. This can take some minutes.
5. Add 'localhost	osmaxx.dev' to your /etc/hosts file
6. Use the configured Apache or start development server (live update after file change)
	1. Live simulation with Apache
		* Open http://osmaxx.dev:8080/excerptExport/ in your local browser
	2. Development
		* Log into vagrant machine: `vagrant ssh`
		* Run development start script: `/var/www/eda/projects/runDevelopmentServer.sh`
		* Open http://osmaxx.dev:8000/excerptExport/ in your local browser


### Reset the box

```shell
vagrant destroy -f
```


### Log into the box

```shell
vagrant ssh
```
or
```shell
ssh -l 'vagrant' -p '2222' 'localhost'
```



## Access

Add

    127.0.0.1   osmaxx.dev
    
to your local /etc/hosts file.

| Feature                       | URL 				                    | Username 	| Password 					|
| ---                           | ---				                    | ---		| ---						|
| Database osmaxx               |					                    | osmaxx	| osmaxx                    |
| App frontend                  | http://osmaxx.dev:8080/excerptexport	|			|							|
| App frontend development      | http://osmaxx.dev:8000/excerptexport	|			|							|
| App backend development       | http://osmaxx.dev:8000/admin          | admin 	| osmaxx					|


## Development

### Run application using Django built in server (see runDevelopmentServer.sh)

You need to specify the ip. Otherwise you are not able to reach the application from outside of the vm.

```shell
#!/bin/bash

CURRENTDIR=`dirname $0`
cd "$CURRENTDIR"
# activate environment
source "../environment/bin/activate"
# get local ip
LOCALIP=`hostname -I`
echo "$LOCALIP"
python ./manage.py runserver "$LOCALIP:8000"
```

### Clear Django cache

```shell
python manage.py shell

# (InteractiveConsole)
from django.core.cache import cache
cache.clear()
```


### Update persistence

#### 1. Update migration information

```shell
cd /path/to/projects/folder
source ../environment/bin/activate
python manage.py makemigrations
```

#### 2. See domain specific migrations (e.g. sql)

```shell
python manage.py sqlmigrate excerptExport {number, e.g. 0001}
```

#### 3. Run migrations on database
```shell
python manage.py migrate
```


### Use backend

#### Create superuser

```shell
python manage.py createsuperuser
```


### Backup & restore the database
```shell
# backup
sudo -u postgres pg_dump osmaxx --data-only > /var/www/eda/data/{yymmdd}-osmaxx-data.sql

# restore
sudo -u postgres psql osmaxx < /var/www/eda/data/{yymmdd}-osmaxx-data.sql
```


### Deployment

#### Package release

```shell
cd toDirectoryContainingOsmaxxRepo
zip -r osmaxx-0.1.zip osmaxx -x *.git* -x *.od* -x *.gitignore* -x *.gitmodules* -x *developmentEnvironment/* -x *data/* -x *.idea* -x *test_db.sqlite* -x *__pycache__*
```
