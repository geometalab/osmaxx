# Releasing a new version

Note: We are not using PyPI (for now?) for making releases.

## Prerequisites

- project setup complete (see [`README.md` > Docker container bootstrapping > Development](/README.md#development-2))
- tests running (see [`testing.md` > Setup](testing.md#setup)) and tests **passing**  
- git flow

## Steps


All these steps can be found in the `release.py` and this can be
used instead of the manual steps `python release.py <version>`.

The steps execute in the script in a nutshell are:

- `git checkout develop`
- `git pull --ff-only`
- `git flow release start <version>`
- `git flow release publish <version>`
- `adapt <version> in osmaxx/__init__.py`
- `python ./web_frontend/manage.py makemessages -l de_CH -l en -l en_UK -l en_US`
- `python ./conversion_service/manage.py makemessages -l de_CH -l en -l en_UK -l en_US`
- `git flow release finish <version>`
- `git push`
- `git push --tags`
- `./build_and_push_images.py`
