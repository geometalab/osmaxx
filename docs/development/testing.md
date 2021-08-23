# Testing

If you want to record (new or recreate) vcr cassettes, before running tests,
start all the services once and let them finish:

## Setup

```bash
source ./activate_local_development
docker-compose up -d --build osm_imorter osmboundaries_importer
docker-compose run --rm frontend sh -c "web_frontend/manage.py createsuperuser"  # enter admin as username and password
docker-compose up --build nginx frontend mediator worker
```

## Linting

Using the instruction below for testing, the flake8 tool is also run.

## Running Tests

For all tests, a redis-server instance is required.

Install testing requirements.

```bash
pip install -r requirements-all.txt
```

Run the tests (using the makefile, which uses the underlying runtests.py), excluding the slow (&sum; > 1 minute) tests:

```bash
make tests-quick
```

If you want to run the slower (mostly sql related tests), it isn't much harder:

```bash
make tests-all
```

You can also use the excellent [tox](http://tox.readthedocs.org/en/latest/) testing tool to run the tests against all supported versions of Python and Django. Install tox globally, and then simply run:

```bash
make tox
```

### Pass arguments to underlying test runner
To pass arguments to `./runtests.py` (which will forward most of them to `pytest`), set `PYTEST_ARGS` for any of the `tests-*` targets:
```bash
make tests-all PYTEST_ARGS="-k test_label_water_l"  #  Only run tests with names that match the
                                                    #  string expression "test_label_water_l".

make tests-all PYTEST_ARGS=test_label_water_l       #  Same as above (magic of ./runtests.py)

make test-quick PYTEST_ARGS=--pdb                   #  Drop to debugger upon each test failure.
```
For command line options of `pytest`, see http://pytest.org/latest/usage.html.

### Cleanup
To clean up all after the tests, you can use

```bash
make clean
```

Which cleans up `__pycache__`, `*.pyc` and docker-containers produced.

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

## Running selenium tests

Prerequisite: a user login with username `admin` and password `admin`. To create this, run the command below:

If haven't already, `source ./activate_local_development`.

```bash
docker-compose run --rm frontend python3 web_frontend/manage.py createsuperuser
```
Enter `admin` as username, you can leave the email blank, then enter `admin` twice for the password.

Run the containers:

```bash
docker-compose up --build -d frontend worker mediator nginx
```

Wait a few minutes for all services to be available, then run all the tests including selenium tests: 

```shell
./runtests.py --driver Firefox
```

If you don't want to have Firefox running in front, under Linux there is a utility which helps in running
this in a separate display: https://github.com/jordansissel/xdotool/blob/master/t/ephemeral-x.sh.

This lets you execute any command in a separate display, and still getting the console output.

For example, using our tests:

```
sudo apt-get install xvfb
wget -nv --show-progress --progress=bar:force:noscroll -c --tries=20 --read-timeout=20 -O /tmp/ephemeral-x.sh https://github.com/jordansissel/xdotool/blob/master/t/ephemeral-x.sh
chmod +x /tmp/ephemeral-x.sh
/tmp/ephemeral-x.sh ./runtests.py --driver Firefox
```
