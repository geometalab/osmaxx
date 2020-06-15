#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import os
import sys
from setuptools import setup


name = 'geometalab.osmaxx'
package = 'osmaxx'
description = 'OSMaxx — OpenStreetMap arbitrary excerpt export'
url = 'https://github.com/geometalab/osmaxx-conversion-service'
author = 'Raphael Das Gupta, Nicola Jordan, Dhruv Sharma, Tobias Blaser, Eugene Phua, Bhavya Chandra, Benedita Tanabi'
author_email = 'geometalab@hsr.ch'
license = 'MIT'


def get_requirements():
    requirements_file_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    # when using tox, requirements.txt doesn't exist in the temp dir created by tox
    if os.path.exists(requirements_file_path):
        try:  # for pip >= 10
            from pip._internal.req import parse_requirements
        except ImportError:  # for pip < 10
            from pip.req import parse_requirements
        parsed_requirements = parse_requirements(requirements_file_path, session=False)
        requirements = [str(ir.req) for ir in parsed_requirements]
    else:
        requirements = []
    return requirements


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("^__version__ = ['\"]([^'\"]+)['\"]",
                     init_py, re.MULTILINE).group(1)


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


version = get_version(package)


if sys.argv[-1] == 'publish':
    if os.system("pip freeze | grep wheel"):
        print("wheel not installed.\nUse `pip install wheel`.\nExiting.")
        sys.exit()
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    print("You probably want to also tag the version now:")
    print("  git tag -a {0} -m 'version {0}'".format(version))
    print("  git push --tags")
    sys.exit()


setup(
    name=name,
    version=version,
    url=url,
    license=license,
    description=description,
    author=author,
    author_email=author_email,
    packages=get_packages(package),
    package_data=get_package_data(package),
    install_requires=get_requirements(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
