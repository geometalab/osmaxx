#!/usr/bin/env python
import subprocess

IMAGES = [
    dict(image_name='geometalab/osmaxx-mediator', dockerfile='Dockerfile.mediator'),
    dict(image_name='geometalab/osmaxx-worker', dockerfile='Dockerfile.worker'),
    dict(image_name='geometalab/osmaxx-frontend', dockerfile='Dockerfile.frontend'),
    dict(image_name='geometalab/osmaxx-nginx', dockerfile='Dockerfile.nginx'),
]


def docker_build(dockerfile, image_name, release, location='.'):
    subprocess.check_call(['docker', 'build', '-f', dockerfile, '-t', '{}:{}'.format(image_name, release), location])


def docker_push(release, image_name, *args, **kwargs):
    subprocess.check_call(['docker', 'push', '{}:{}'.format(image_name, release)])


if __name__ == '__main__':
    release = subprocess.check_output(["git", "describe", "--dirty"]).strip().decode()
    for image in IMAGES:
        docker_build(release=release, **image)
    for image in IMAGES:
        docker_push(release=release, **image)
    print(release, ' has been pushed, you can now use that in your deployment!')
