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

## Running the test-suite and integration tests

There's a Python 3 script to facilitate testing including some docker integration tests.

It allows some control over what tests to run. Call it with
```shell
./runtests.py --help
```
to see what options it provides.

To run tests of all available test types, call it without passing any options (be sure to read the part about
running end to end test before you are doing this!):
```shell
./runtests.py
```

## Running end to end tests (e2e)

### Warnings 

* before doing anything, you *MUST* run `docker-compose run --rm osmplanet` to have the pbf data at hand!
* It needs a Firefox browser installed (for now)
* These run for quite a long time (over five Minutes!). 
* The containers are being destroyed at the beginning (creating a clean state). Resulting in
    * Only run one test at a time
    * don't run on production!
    * don't run docker-compose in parallel
    * exiting data is being destroyed 

### Prerequisites

An activated virtualenv with requests installed.

```shell
virtualenv tmp
. ./tmp/bin/activate
pip install -r e2e/requirements.txt
python e2e/e2e_tests.py
```
or
```shell
RUN_E2E=true ./runtests.py
```
or
```shell
./runtests.py --end-to-end-tests
```

To simplify the steps needed, the `runtests.py` can be used to run all tests, as described in the next section.
 
## Running all tests

**Warnings**:

* same rules as running e2e test apply
* it will usually take more than 7 minutes to finish
* it will create a temporary virtualenv and remove it afterwards again

```shell
./runtests.py
```


## Generating the test coverage html

```shell
docker-compose run webapp bash -c "DJANGO_SETTINGS_MODULE=config.settings.test coverage run --source='.' manage.py test;coverage html"
``` 

and then open the directory `web_frontend/htmlcov/index.html` in a browser.

