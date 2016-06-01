#!/usr/bin/env python
import argparse
import os
import subprocess

from build_and_push_images import IMAGES, docker_build, docker_push


def ask_yes_no(question):
    if input(question).lower().strip()[0] == "y":
        return True
    return False


def continue_or_stop(text):
    print(text)
    if not ask_yes_no("are you sure to continue? (y/n) "):
        print("exiting.")
        exit(0)


def execute(command, shell=False):
    if isinstance(command, str):
        command = command.split()
    subprocess.check_call(command, shell=shell)


def execute_steps(steps):
    for step in steps:
        execute(step)


def build_and_push_images(release_version):
    for image in IMAGES:
        docker_build(release=release_version, **image)
    for image in IMAGES:
        docker_push(release=release_version, **image)


def prepare_for_release(release_version):
    execute_steps([
        "git checkout develop",
        "git pull --ff-only",
        "git flow release start {}".format(release_version),
    ])


def make_release_specific_changes(release_version):
    execute_steps([
        "python ./web_frontend/manage.py makemessages -l de_CH -l en -l en_UK -l en_US",
        "python ./osmaxx_conversion_service/manage.py makemessages -l de_CH -l en -l en_UK -l en_US",
        ["git", "commit", "-m", 'added makemessages output', 'osmaxx/locale'],
    ])
    version_file_path = os.path.join(os.path.dirname(__file__), 'osmaxx', '__init__.py')
    with open(version_file_path, 'r') as version_file:
        version_file_content = version_file.readlines()
    with open(version_file_path, 'w') as version_file:
        for line in version_file_content:
            if line.startswith('__version__'):
                line = "__version__ = '{}'".format(release_version)
            version_file.write(line)
    print("""Is the version file correct
    {}
    ?
    """.format(execute("git diff osmaxx/__init__.py")))
    execute(["git", "commit", "-m", 'bump version to {}'.format(release_version), 'osmaxx/__init__.py'])


def release_finish(release_version):
    execute_steps([
        ["git", "flow", "release", "finish", release_version, "-m", "'OSMaxx release {}'".format(release_version)],
        "git push",
        "git push --tags",
    ])
    build_and_push_images(release_version)


def release_done():
    print("""
---------------------------------
release {} finished
You can now use this
""".format(release_version))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('release', type=str, help='version to be released')
    args = parser.parse_args()
    release_version = args.release

    continue_or_stop("You want to make a new release {}".format(release_version))

    prepare_for_release(release_version)
    make_release_specific_changes(release_version)

    continue_or_stop("Should be continued to push the release to the repository?")
    release_finish(release_version)

    release = subprocess.check_output(["git", "describe", "--dirty"]).strip().decode()
    if release != release_version:
        continue_or_stop("Your release number ({}) is not the same as the one on the"
                         "repository ({}).".format(release_version, release))
    release_done()
