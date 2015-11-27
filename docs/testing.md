# Testing

## Running the standard test-suite

running locally, in the `osmaxx-py` directory (using a virtualenv):

```shell
DJANGO_SETTINGS_MODULE=config.settings.test ./manage.py test
```

### Notice

Since the ampq Service is not available, you'll get a 4 failing tests. Therefore it is recommended to
run them in a docker container, as described below.

Using docker and docker-compose:
 
```shell
docker-compose run --rm webappdev bash -c 'DJANGO_SETTINGS_MODULE=config.settings.test ./manage.py test'
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
docker-compose run webappdev bash -c "DJANGO_SETTINGS_MODULE=config.settings.test coverage run --source='.' manage.py test;coverage html"
``` 

and then open the directory `osmaxx-py/htmlcov/index.html` in a browser.

