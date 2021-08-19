#!/usr/bin/env python3
import os
import subprocess
import shutil
import time

import datetime

import sentry_sdk
from sentry_sdk import capture_exception


BASE_DIR = "/var/data/osm-planet"
PBF_DIR = os.path.join(BASE_DIR, "pbf")
PLANET_LATEST = os.path.join(PBF_DIR, "planet-latest.osm.pbf")
PLANET_LATEST_ON_UPDATE = os.path.join(PBF_DIR, "new_planet-latest.osm.pbf")
NICE = ["nice", "-n", "19"]
OSM_PLANET_PATH_RELATIVE_TO_MIRROR = os.environ.get(
    "osm_planet_path_relative_to_mirror", "/pbf/planet-latest.osm.pbf"
)
OSM_PLANET_MIRROR = os.environ.get(
    "osm_planet_mirror",
    "https://ftp.gwdg.de/pub/misc/openstreetmap/planet.openstreetmap.org",
)


def planet_url():
    return OSM_PLANET_MIRROR + OSM_PLANET_PATH_RELATIVE_TO_MIRROR


def full_download(complete_planet_mirror_url):
    os.makedirs(PBF_DIR, exist_ok=True)
    download_pbf_path = "{}_tmp".format(PLANET_LATEST)
    download_command = [
        "wget",
        "--continue",
        "-O",
        download_pbf_path,
        complete_planet_mirror_url,
    ]
    subprocess.check_call(NICE + download_command)
    shutil.move(download_pbf_path, PLANET_LATEST)


def update(osmupdate_extra_params):
    update_comand = (
        ["osmupdate", "-v"]
        + osmupdate_extra_params.split()
        + [PLANET_LATEST, PLANET_LATEST_ON_UPDATE]
    )
    try:
        subprocess.check_call(NICE + update_comand)
    except subprocess.CalledProcessError as e:
        # if the file is alright, but already up-to-date we want to continue, not stop!
        #  http://m.m.i24.cc/osmupdate.c
        #     if(loglevel>0)
        #       PINFO("Creating output file.")
        #     strcpy(stpmcpy(master_cachefile_name,global_tempfile_name,
        #       sizeof(master_cachefile_name)-5),".8");
        #     if(!file_exists(master_cachefile_name)) {
        #       if(old_file==NULL)
        #         PINFO("There is no changefile since this timestamp.")
        #       else
        #         PINFO("Your OSM file is already up-to-date.")
        # return 21;
        if e.returncode == 21:
            return
        else:
            raise
    shutil.move(PLANET_LATEST_ON_UPDATE, PLANET_LATEST)


def _is_night_time(now):
    return now.hour < 4 or now.hour > 22


def run(*, sleep_seconds=10, osmupdate_extra_params):
    last_full_download_time = datetime.datetime.min
    while True:
        now = datetime.datetime.now()
        full_update_is_due = now - last_full_download_time > datetime.timedelta(weeks=1)
        if (
            not os.path.exists(PLANET_LATEST)
            or full_update_is_due
            and _is_night_time(now)
        ):
            full_download(planet_url())
            last_full_download_time = datetime.datetime.now()
        # start updating immediately
        update(osmupdate_extra_params)
        print("update done, sleeping for {} seconds".format(sleep_seconds))
        # wait for this seconds
        time.sleep(sleep_seconds)


def run_with_sentry(callable, *args, **kwargs):
    try:
        callable(*args, **kwargs)
    except Exception as e:
        capture_exception(e)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--wait-seconds",
        type=int,
        default=120,
        help="wait this amount of seconds between updates",
    )
    args = parser.parse_args()
    sleep_seconds = args.wait_seconds
    update_extra_params = os.environ.get("osmupdate_extra_params", "")

    sentry_dsn = os.environ.get("SENTRY_DSN", None)
    if sentry_dsn is not None:
        sentry_sdk.init(sentry_dsn)
        run_with_sentry(
            run, sleep_seconds=sleep_seconds, osmupdate_extra_params=update_extra_params
        )
    else:
        run(sleep_seconds=sleep_seconds, osmupdate_extra_params=update_extra_params)
