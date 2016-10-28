#!/usr/bin/env python3
import os
import subprocess
import shutil
import time

from raven import Client


BASE_DIR = '/var/data/osm-planet'
PBF_DIR = os.path.join(BASE_DIR, 'pbf')
PLANET_LATEST = os.path.join(PBF_DIR, 'planet-latest.osm.pbf')
PLANET_LATEST_ON_UPDATE = os.path.join(PBF_DIR, 'new_planet-latest.osm.pbf')
NICE = ["nice", "-n", "19"]
OSM_PLANET_PATH_RELATIVE_TO_MIRROR = os.environ.get(
    'osm_planet_path_relative_to_mirror', '/pbf/planet-latest.osm.pbf'
)
OSM_PLANET_MIRROR = os.environ.get(
    'osm_planet_mirror', 'http://ftp.gwdg.de/pub/misc/openstreetmap/planet.openstreetmap.org'
)


def planet_url():
    return OSM_PLANET_MIRROR + OSM_PLANET_PATH_RELATIVE_TO_MIRROR


def initial_download(complete_planet_mirror_url):
    os.makedirs(PBF_DIR, exist_ok=True)
    download_pbf_path = "{}_tmp".format(PLANET_LATEST)
    download_command = ["wget", "--continue", "-O", download_pbf_path, complete_planet_mirror_url]
    subprocess.check_call(NICE + download_command)
    shutil.move(download_pbf_path, PLANET_LATEST)


def update(osmupdate_extra_params):
    update_comand = ["osmupdate", "-v"] + osmupdate_extra_params.split() + [PLANET_LATEST, PLANET_LATEST_ON_UPDATE]
    subprocess.check_call(NICE + update_comand)
    shutil.move(PLANET_LATEST_ON_UPDATE, PLANET_LATEST)


def run(*, sleep_seconds=10, osmupdate_extra_params=None):
    while True:
        # no loss, whenever we start the container up, we download the newest pbf and start updating it.
        initial_download(planet_url())
        # start updating immediately
        update(osmupdate_extra_params)
        print("update done, sleeping for {} seconds".format(sleep_seconds))
        # wait for this seconds
        time.sleep(sleep_seconds)


def run_with_sentry(callable, *args, sentry_dsn, **kwargs):
    client = Client(sentry_dsn)
    release = os.environ.get('SENTRY_RELEASE', 'unknown')
    try:
        callable(*args, **kwargs)
    except:
        client.user_context({'release': release})
        client.captureException()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--wait-seconds",
                        type=int, default=120,
                        help="wait this amount of seconds between updates")
    args = parser.parse_args()
    sleep_seconds = args.wait_seconds
    update_extra_params = os.environ.get('osmupdate_extra_params', '')

    sentry_dsn = os.environ.get('SENTRY_DSN', None)
    if sentry_dsn is not None:
        run_with_sentry(run, sentry_dsn=sentry_dsn, sleep_seconds=sleep_seconds, osmupdate_extra_params=update_extra_params)
    else:
        run(sleep_seconds=sleep_seconds, osmupdate_extra_params=update_extra_params)
