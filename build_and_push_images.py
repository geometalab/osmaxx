#!/usr/bin/env python
import subprocess
from time import sleep

IMAGES = [
    dict(
        image_name="geometalab/osmaxx-worker",
        context="src/",
        dockerfile="docker/Dockerfile",
        target="worker",
    ),
    dict(
        image_name="geometalab/osmaxx-scheduler",
        context="src/",
        dockerfile="docker/Dockerfile",
        target="scheduler",
    ),
    dict(
        image_name="geometalab/osmaxx-setup",
        context="src/",
        dockerfile="docker/Dockerfile",
        target="setup",
    ),
    dict(
        image_name="geometalab/osmaxx-file-purge",
        context="src/",
        dockerfile="docker/Dockerfile",
        target="file-purge",
    ),
    dict(
        image_name="geometalab/osmaxx-worker-db",
        context="docker-helper-images/osmaxx-postgis-translit/",
        dockerfile="docker-helper-images/osmaxx-postgis-translit/Dockerfile",
    ),
    dict(
        image_name="geometalab/osm-pbf-updater",
        context="docker-helper-images/osm_pbf_updater/",
        dockerfile="docker-helper-images/osm_pbf_updater/Dockerfile",
    ),
    # osmboundaries needs special files,
    # to udpate please follow the instructions there
    # (especially regarding the update_shaepfiles.sh!)
]


def docker_build(dockerfile, image_name, release, context='.', target=None):
    command = [
        "docker",
        "build",
        "--pull",
        "-f",
        f"{dockerfile}",
    ]
    if target:
        command.extend(["--target", target])
    command.extend(
        [
            "-t",
            "{}:{}".format(image_name, release),
            context,
        ]
    )
    subprocess.check_call(command)


def docker_push(release, image_name, *args, **kwargs):
    subprocess.check_call(["docker", "push", "{}:{}".format(image_name, release)])


if __name__ == "__main__":
    is_dirty = subprocess.check_output(["git", "diff", "--stat"]).strip().decode()
    git_version = subprocess.check_output(["git", "describe", "--tags", "--dirty"]).strip().decode()
    release = subprocess.check_output(["poetry", "version"], cwd='src/').strip().decode().replace('osmaxx ', '')

    print()
    print(f'Version Info')
    print(f'git version (latest tag): {git_version}')
    print(f'release version (pyproject.toml): {release}')
    print('**release has precedence over tag for image tag name**')
    
    if git_version != release:
        release = f'{release}-dev'
    if is_dirty:
        release = f'{release}-dirty'
    
    print()
    print(f'using {release} as tag')
    
    print('press ctrl-c within 4 seconds to stop this process')
    # 10 seconds is just in between too long for an information, and
    # still long enough to (read and then) press ctrl-c
    print()
    sleep(10)
    
    for image in IMAGES:
        docker_build(release=release, **image)
    for image in IMAGES:
        docker_push(release=release, **image)

    # release versions that do not contain breaking changes
    if git_version == release:
        shorter_release = release[:-2]
        for image in IMAGES:
            docker_build(release=shorter_release, **image)
        for image in IMAGES:
            docker_push(release=shorter_release, **image)
        shorter_release = shorter_release[:-2]
        for image in IMAGES:
            docker_build(release=shorter_release, **image)
        for image in IMAGES:
            docker_push(release=shorter_release, **image)

    print(release, " has been pushed, you can now use that in your deployment!")
