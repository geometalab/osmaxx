# Project Development Environment (Docker)

## Local prerequisites

| dependency | supported versions | Installation recommendation for Ubuntu 14.04 |
| ---------- | ------------------ | ---------------------------------------------|
| <a name='dependency_docker'>docker</a> | 1.10 (1.9 may still work, too) | Follow [the official Docker installation instructions for Ubuntu Linux](https://docs.docker.com/engine/installation/linux/ubuntulinux/) |
| <a name='dependency_docker-compose'>docker-compose</a> | 1.6 | Install system-wide via <a href='#dependency_pip'>`pip`</a> (**not** via `pip3`! `docker-compose` is implemented in Python 2.): <pre class="highlight highlight-source-shell">sudo pip install docker-compose</pre> |
| <a name='dependency_pg_config'>pg_config</a> (required by psycopg2) |  | <pre class="highlight highlight-source-shell">sudo apt install libpq-dev</pre> |
| <a name='dependency_python3'>Python 3</a> | 3.4 | Would be pulled in by `python3-gdal` or <a href='#dependency_python3-dev'>`python3-dev`</a>, but you should install it explicitly with <pre class="highlight highlight-source-shell">sudo apt install python3</pre> |
| <a name='dependency_requirements.txt'>various PyPI packages</a> | See [`requirements-all.txt`](/requirements-all.txt) | Install in a Python 3 [virtual environment](#dependency_venv). Create one with e.g. <pre class="highlight highlight-source-shell">mkdir -p ~/.virtualenvs && \\<br />virtualenv ~/.virtualenvs/osmaxx -p python3</pre> activate it with <pre class="highlight highlight-source-shell">source ~/.virtualenvs/osmaxx/bin/activate</pre> Then, in the same shell session, use [`pip3`](#dependency_pip3) to install the packages: <pre class="highlight highlight-source-shell"># run from this repo's root dir<br />pip3 install -r requirements-all.txt</pre><hr>`virtualenvwrapper` users can perform all of the above in a single step: <pre class="highlight highlight-source-shell"># run from this repo's root dir<br />mkvirtualenv -r requirements-all.txt \\<br />             -a . -p $(which python3) osmaxx</pre>The `-a .` will also [associate the repo root as the project directory](http://virtualenvwrapper.readthedocs.org/en/latest/command_ref.html#mkvirtualenv) of the new Python 3 virtual environemnt. |
| <a name='dependency_pip3'>pip3</a> |  | Provided by <a href='#dependency_venv'>virtualenv</a> in the virtual Python environments it creates. |
| <a name='dependency_venv'>virtualenv</a> (Python 2 and 3) |  | Install system-wide with <pre class="highlight highlight-source-shell">sudo apt install python-virtualenv</pre> |
| <a name='dependency_python3-dev'>Python 3 C bindings</a> | 3.4 | Would be pulled in by `python3-gdal`, but you should install it explicitly with <pre class="highlight highlight-source-shell">sudo apt install python3-dev</pre> | 
| <a name='dependency_geos_c'>GEOS C library</a> | whatever [GeoDjango supports](https://docs.djangoproject.com/en/1.10/ref/contrib/gis/install/geolibs/#installing-geospatial-libraries) | <pre class="highlight highlight-source-shell">sudo apt install python3-gdal</pre> will pull this and other required libraries in. `python3-gdal` itself is not required. Thus, if you prefer a more minimal installation, only install `libgeos-c1`. |
| <a name='dependency_gdal'>GDAL library</a> | whatever [GeoDjango supports](https://docs.djangoproject.com/en/1.10/ref/contrib/gis/install/geolibs/#installing-geospatial-libraries) | <pre class="highlight highlight-source-shell">sudo apt install python3-gdal</pre> will pull this and other required libraries in. `python3-gdal` itself is not required. Thus, if you prefer a more minimal installation, only install `libgdal1h`. |
| <a name='dependency_pip'>pip</a> (Python 2) |  | <pre class="highlight highlight-source-shell">sudo apt install python-pip</pre> |

For committing and using the pre-commit hook (which really should be used) flake8 needs to be installed on
the local system/machine.

For Ubuntu and Debian this is:

```shell
sudo apt-get install python3-flake8
```

Then the pre-commit hook can be linked to the hooks.

```shell
cd <osmaxx-repo-root>
ln -s ../../hooks/pre-commit .git/hooks/pre-commit
```

### Python package management

We use [`pip-tools`](https://github.com/nvie/pip-tools#readme) to manage the PyPI packages we depend on.
It shouldn't matter whether you install `pip-tools` globally or within the `osmaxx` virtualenv.

Once `pip-tools` is installed, try running `pip-sync` in your `osmaxx` virtualenv.
If it tells you to upgrade or downgrade `pip` do as instructed (also in the virtualenv)
and repeat until `pip-sync` doesn't complain anymore.
(You can ignore warnings about a newer pip version being available.)

#### Syncing installed python packages

`pip-tools` implicitly pins package versions, so they are synchronous between developers.
The thusly fixed versions are tracked in the `*requirements*.txt` files.
Running
```bash
pip-sync *requirements*.txt
```
in your virtualenv will install, uninstall, up- and downgrade packages
as neccessary to make your virtualenv match the packages listed in _all_ these files.
You'll want to do this, whenever the `*.txt*` files have changed,
e.g. due to pulling in commits or switching branches.

Note that in staging and production,
only the content of `requirements.txt` (not of `requirements-all.txt`) should be installed.
(The [docker containers](#using-the-project-docker-setup) already take care of that.)

#### Changing requirements

We track top-level requirements and explicitly pinned versions in `*requirements*.in` files.
If you've changed one of those, run
```bash
pip-compile <the changed *.in file>
```
e.g.
```bash
pip-compile requirements-local.in
```
to update the corresponding `*.txt` file.
This will also upgrade the versions listed in that `*.txt` file to the greatest ones available on PyPI
(within the range allowed in the `*requirements*.in` file). 

To compile the `*requirements*.txt` files for _all changed_ `*requirements*.in`
**and** sync the new versions to your virtualenv in one go,
you may use our handy GNU make target:
```bash
make pip-sync-all
```

#### Upgrade package versions

To upgrade the implicitly pinned versions of all dependencies to the greatest ones available on PyPI
(within the range allowed in the `*requirements*.in` files)
run
```bash
make pip-upgrade
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
docker-compose run webapp /bin/bash
```


## Run all tests
(Requires Python 3 on the host.)

```shell
./runtests.py
```

To run the application tests only, see [Commonly used commands while developing / Run tests](useful-commands.md#run-tests).


## Access the application

`http://<your_ip>:8889`

where `<your_ip>` is your (public) IP as reported by
```bash
ip route get 1 | awk '{print $NF;exit}'
```

You can generate the complete URL in `sh` with:
```bash
echo "http://$(ip route get 1 | awk '{print $(NF-2);exit}'):8889"
```

## Enable development with debug toolbar enabled

In your `docker-compose.yml` file, add a line containing the content of the command:
```
echo $(ip -4 addr show docker0 | grep -Po 'inet \K[\d.]+')
```

Add that to the docker-compose.yml:

```
webapp:
   ...
   environment:
   ...
    - DJANGO_INTERNAL_IPS=172.17.42.1 # IP from the command above
```
### Note: More automatic in docker-compose 1.5
Once **docker-compose 1.5** or better is being used, you can simplify this process by letting docker-compose evaluate the command for you:

See https://github.com/docker/compose/pull/1765.

Then one should be able to use:

`- DJANGO_INTERNAL_IPS=$(ip -4 addr show docker0 | grep -Po 'inet \K[\d.]+')`

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
`docker-compose build --no-cache webapp`.


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
## Emails sending

Emails during development and testing can be found locally under `/tmp/osmaxx-development-emails`. 
This directory holds all sent emails.

If you should find yourself in need of changing the email settings, please
have a look at the django settings for emails: 
[Django email settings](https://docs.djangoproject.com/en/1.8/ref/settings/#email-backend)

To change them, prepend `DJANGO_` to the settings name and add it to the environment in the `compose-development.yml`.

The following list ist supported:

```
    - DJANGO_EMAIL_FILE_PATH=/dev-emails
    - DJANGO_EMAIL_BACKEND=django.core.mail.backends.filebased.EmailBackend
    - DJANGO_EMAIL_HOST=localhost
    - DJANGO_EMAIL_HOST_PASSWORD=''
    - DJANGO_EMAIL_HOST_USER=''
    - DJANGO_EMAIL_PORT=25
    - DJANGO_EMAIL_SUBJECT_PREFIX='[OSMaxx-dev] '
    - DJANGO_EMAIL_USE_TLS=False
    - DJANGO_EMAIL_USE_SSL=False
    - DJANGO_EMAIL_TIMEOUT=None
    - DJANGO_EMAIL_SSL_CERTFILET=None
    - DJANGO_EMAIL_SSL_KEYFILE=None
```
