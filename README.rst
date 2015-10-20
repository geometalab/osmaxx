osmaxx-conversion-service
=========================

|build-status-image| |pypi-version|

Overview
--------

Conversion service API Frontend for Osmaxx

Requirements
------------

-  Python (3.3, 3.4)
-  Django (1.8)
-  Django REST Framework (3.2)

Installation
------------

Install using ``pip``\ …

.. code:: bash

    $ pip install osmaxx-conversion-service

Example
-------

TODO: Write example.

Testing
-------

Install testing requirements.

.. code:: bash

    $ pip install -r requirements.txt

Run with runtests.

.. code:: bash

    $ ./runtests.py

You can also use the excellent `tox`_ testing tool to run the tests
against all supported versions of Python and Django. Install tox
globally, and then simply run:

.. code:: bash

    $ tox

Documentation
-------------

To build the documentation, you’ll need to install ``mkdocs``.

.. code:: bash

    $ pip install mkdocs

To preview the documentation:

.. code:: bash

    $ mkdocs serve
    Running at: http://127.0.0.1:8000/

To build the documentation:

.. code:: bash

    $ mkdocs build

.. _tox: http://tox.readthedocs.org/en/latest/

.. |build-status-image| image:: https://secure.travis-ci.org/geometalab/osmaxx-conversion-service.svg?branch=master
   :target: http://travis-ci.org/geometalab/osmaxx-conversion-service?branch=master
.. |pypi-version| image:: https://img.shields.io/pypi/v/osmaxx-conversion-service.svg
   :target: https://pypi.python.org/pypi/osmaxx-conversion-service


Register on PyPI
----------------

$ python setup.py register

New release on PyPI
-------------------

$ python setup.py publish
You probably want to also tag the version now:
      git tag -a 0.1.0 -m 'version 0.1.0'
      git push --tags
