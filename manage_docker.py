#!/usr/bin/env python3
import subprocess
import time

RUN = ["docker-compose", "run"]
SOURCE = RUN + ["source"]
WEBAPP = RUN + ["webapp"]
WEBAPP_MANAGE = WEBAPP + ["python3", "manage.py"]
STATIC = RUN + ["static"]
MEDIA = RUN + ["media"]
CELERY = RUN + ["celery"]
DATABASE = RUN + ["database"]

def _remove_requirements():
    subprocess.call(["rm", "-r", "docker/celery/requirements"])
    subprocess.call(["rm", "-r", "docker/webapp/requirements"])

def _copy_requirements():
    subprocess.call(["cp", "-r", "osmaxx/requirements", "docker/celery/requirements"])
    subprocess.call(["cp", "-r", "osmaxx/requirements", "docker/webapp/requirements"])

def _build_container(container=None):
    if container is None:
        subprocess.call(["docker-compose", "build"])
    else:
        subprocess.call(["docker-compose", "build", container])

def _migrate():
    print("executing migrations")
    subprocess.call(["docker-compose", "up", "-d", "database"])
    # wait for the database cluster to come online
    time.sleep(15)
    print("applying migrations")
    subprocess.call(WEBAPP_MANAGE + ["migrate"])

def _create_super_user():
     subprocess.call(WEBAPP_MANAGE + ["createsuperuser"])

def bootstrap():
    print("boostrapping the containers")
    _copy_requirements()
    _build_container()
    _remove_requirements()
    _migrate()
    _create_super_user()

def update(container=None):
    print("updating containers")
    _copy_requirements()
    _build_container(container)
    _remove_requirements()
    if container is None:
        _migrate()


def run(container=None):
    print("press Ctrl+c to cancel")
    if container is None:
        print("running all containers")
        subprocess.call(["docker-compose", "up"])
    else:
        print("running " + container)
        subprocess.call(["docker-compose", "up", "%s" % container])

ACTIONS = {
    'run': run,
    'migrate': _migrate,
    'update': update
}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--bootstrap",
                        action='store_true',
                        help="first initial setup of the containers, implies `update`")
    parser.add_argument("-u", "--update",
                        action='store_true',
                        help="update the containers, execute django migrations")
    parser.add_argument("action", help="Choose one: %s" % ', '.join(ACTIONS.keys()))
    parser.add_argument("-c", "--container",
                        help="container name (as defined in docker-compose.yml")
    args = parser.parse_args()
    if args.bootstrap:
        bootstrap()
    if args.update:
        update(args.container)
    if args.action:
        if args.action in ACTIONS:
            ACTIONS[args.action](args.container)
