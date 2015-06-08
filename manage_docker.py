#!/usr/bin/env python3
import subprocess
import time


SOURCE = "source"
WEBAPP = "webapp"
STATIC = "static"
MEDIA = "media"
CELERY = "celery"
DATABASE = "database"

CONTAINERS = [
    SOURCE,
    WEBAPP,
    STATIC,
    MEDIA,
    CELERY,
    DATABASE,
]

RUN = ["docker-compose", "run"]

WEBAPP_MANAGE = RUN + [WEBAPP] + ["python3", "manage.py"]

def _remove_requirements(container):
    subprocess.call(["rm", "-r", "docker/" + container + "/requirements"])

def _copy_requirements(container):
    subprocess.call(["cp", "-r", "osmaxx/requirements", "docker/" + container + "/requirements"])

def _build_container(container, from_scratch=False):
    if from_scratch:
        subprocess.call(["docker-compose", "build", "--no-cache", container])
    else:
        subprocess.call(["docker-compose", "build", container])

def _migrate(container):
    # can only apply migrations to container webapp (django app)
    if container == WEBAPP:
        print("executing migrations")
        subprocess.call(["docker-compose", "up", "-d", "database"])
        # wait for the database cluster to come online
        time.sleep(15)
        print("applying migrations")
        subprocess.call(WEBAPP_MANAGE + ["migrate"])

def _create_super_user(container):
    # can only apply create a superuser in the webapp container (django app)
    if container == WEBAPP:
        subprocess.call(WEBAPP_MANAGE + ["createsuperuser"])

def _bootstrap(container, no_cache):
    _copy_requirements(container)
    _build_container(container, no_cache)
    _remove_requirements(container)
    if container in [WEBAPP, CELERY]:
        _migrate(container)
        _create_super_user(container)

def _update(container):
    print("updating containers")
    _copy_requirements(container)
    _build_container(container)
    _remove_requirements(container)
    _migrate(container)

def bootstrap(container=None, from_scratch=False):
    print("bootstrapping the containers")
    if container is None:
        for container in CONTAINERS:
            _bootstrap(container, from_scratch)
    else:
        _bootstrap(container, from_scratch)

def up(container=None):
    print("press Ctrl+c to cancel")
    if container:
        print("running " + container)
        subprocess.call(["docker-compose", "up", "%s" % container])
    else:
        print("running all containers")
        subprocess.call(["docker-compose", "up"])

def update(container=None):
    if container:
        _update(container)
    else:
        for container in CONTAINERS:
            _update(container)

def migrate(container=None):
    if container:
        _migrate(container)
    else:
        _migrate(WEBAPP)

def stop(container=None):
    if container:
        subprocess.call(["docker-compose", "stop", "%s" % container])
    else:
        subprocess.call(["docker-compose", "stop"])

def clean(container=None):
    if container:
        subprocess.call(["docker-compose", "stop", "%s" % container])
        subprocess.call(["docker-compose", "kill", "%s" % container])
        subprocess.call(["docker-compose", "rm", "%s" % container])
    else:
        subprocess.call(["docker-compose", "stop"])
        subprocess.call(["docker-compose", "kill"])
        subprocess.call(["docker-compose", "rm"])

def destroy(container=None):
    if container:
        subprocess.call(["docker", "rm", "%s" % container])
        subprocess.call(["docker-compose", "kill", "%s" % container])
        subprocess.call(["docker-compose", "rm", "%s" % container])
    else:
        subprocess.call(["docker-compose", "stop"])
        subprocess.call(["docker-compose", "kill"])
        subprocess.call(["docker-compose", "rm"])

ACTIONS = {
    'bootstrap': bootstrap,
    'run': up,
    'update': update,
    'migrate': migrate,
    'stop': stop,
    'clean': clean,
    'destroy': destroy,
}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("action", help="Choose one: %s" % ', '.join(ACTIONS.keys()))
    parser.add_argument("-c", "--container",
                        help="container name (as defined in docker-compose.yml")
    parser.add_argument("--from-scratch",
                        action='store_true',
                        help="ignored for any other command other than `bootstrap`." +
                             "Ignores all cached images from docker.")
    args = parser.parse_args()
    if args.action:
        if args.action in ACTIONS:
            if args.from_scratch:
                if args.action == 'bootstrap':
                    ACTIONS[args.action](args.container, True)
                # ignore all other
            else:
                ACTIONS[args.action](args.container)
