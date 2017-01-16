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


## Running selenium tests

Prerequisite: a user login with username `admin` and password `admin`. To create this, run the command below:

If haven't already, `source ./activate_local_development`.

```bash
docker-compose -f docker-compose-tests.yml run --rm frontend python3 web_frontend/manage.py createsuperuser
```
Enter `admin` as username, you can leave the email blank, then enter `admin` twice for the password.

Run the containers:

```bash
docker-compose -f docker-compose-tests.yml up --build -d frontend worker mediator nginx
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
wget -O /tmp/ephemeral-x.sh https://github.com/jordansissel/xdotool/blob/master/t/ephemeral-x.sh
chmod +x /tmp/ephemeral-x.sh
/tmp/ephemeral-x.sh ./runtests.py --driver Firefox
```

