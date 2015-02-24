# Project Development Environment


# Features

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
3. Download and install rsync
	* Ubuntu:
	
		```shell
		sudo apt-get install rsync
		```
3. Navigate to "developmentEnvironment", run "vagrant up && vagrant rsync-auto" to start bring up the machine
4. On first start up, Vagrant will download the box. This can take some minutes.
5. Add 'osmaxx.dev localhost' to your /etc/hosts file


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

| Feature 			| URL 				| Username 	| Password 					|
| ---				| ---				| ---		| ---						|
| Database osmaxx	|					| osmaxx	| I1eruI2q7pDSi5JSTgyWBHto	|
| Web Frontend App	| osmaxx.dev:8080	|			|							|


## Run application using Django built in server

You need to specify the ip. Otherwise you are not able to reach the application from outside of the vm.

```shell
# get local ip
LOCALIP = ifconfig | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p'

# activate environment
cd "/path/to/manage.py"
source "../environment/bin/activate"

# run server. Replace $localIP by the ip address of the vm if you run this manually
python manage.py runserver "$LOCALIP:8000"
```


## Update persistence

### Update migration information

```shell
cd /path/to/projects/folder
source ../environment/bin/activate
python manage.py makemigrations
```

### See domain specific migrations (e.g. sql)

```shell
python manage.py sqlmigrate excerptExport 0001
```

### Run migrations on database
```shell
python manage.py migrate
```


## Use backend

### Create superuser

```shell
python manage.py createsuperuser
```