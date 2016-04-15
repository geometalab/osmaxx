# Testing

If you want to record (new or recreate) vcr cassettes, before running tests,
start all the services once and let them finish:

```bash
docker-compose up
```

## Running the standard test-suite

Required environment:
```shell
sudo apt-get install python3 libpq-dev python3-dev

virtualenv-3.{version} .venv
source .venv/bin/activate
pip3 install -r web_frontend/requirements/local.txt
```

Testrunner:
```shell
DJANGO_SETTINGS_MODULE=config.settings.test ./web_frontend/manage.py test
```

## Running the test-suite

There's a Python 3 script to facilitate testing.

It allows some control over what tests to run. Call it with
```shell
./runtests.py --help
```
to see what options it provides.


### Running all tests

**Warning**: This will usually take more than 7 minutes to finish

To run tests of all available test types, call the script without passing any options:

```shell
./runtests.py
```


## Generating the test coverage html

```shell
docker-compose run webapp bash -c "DJANGO_SETTINGS_MODULE=config.settings.test coverage run --source='.' manage.py test;coverage html"
``` 

and then open the directory `web_frontend/htmlcov/index.html` in a browser.

