#!/usr/bin/env python
import subprocess

IMAGES = [
    dict(
        image_name="geometalab/osmaxx-mediator",
        dockerfile="Dockerfile",
        target="mediator",
    ),
    dict(
        image_name="geometalab/osmaxx-worker",
        dockerfile="Dockerfile",
        target="worker",
    ),
    dict(
        image_name="geometalab/osmaxx-frontend",
        dockerfile="Dockerfile",
        target="frontend",
    ),
    dict(
        image_name="geometalab/osm-pbf-updater",
        dockerfile="osm_pbf_updater/Dockerfile",
        location="docker-helper-images/osm_pbf_updater/",
    ),
    dict(
        image_name="geometalab/osmaxx-postgis-translit",
        dockerfile="osm_pbf_updater/Dockerfile",
        location="docker-helper-images/osmaxx-postgis-translit/",
    ),
]


def docker_build(dockerfile, image_name, release, location=".", target=None):
    command = [
        "docker",
        "build",
        "--pull",
        "-f",
    ]
    if target:
        command.extend(["--target", target])
    command.extend(
        [
            dockerfile,
            "-t",
            "{}:{}".format(image_name, release),
            location,
        ]
    )
    subprocess.check_call(command)


def docker_push(release, image_name, *args, **kwargs):
    subprocess.check_call(["docker", "push", "{}:{}".format(image_name, release)])


if __name__ == "__main__":
    release = subprocess.check_output(["git", "describe", "--dirty"]).strip().decode()
    for image in IMAGES:
        docker_build(release=release, **image)
    for image in IMAGES:
        docker_push(release=release, **image)
    print(release, " has been pushed, you can now use that in your deployment!")
