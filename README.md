# OSMaxx

[![Build Status](https://travis-ci.org/geometalab/osmaxx.svg?branch=master)](https://travis-ci.org/geometalab/osmaxx) ([branch `master`](https://github.com/geometalab/osmaxx/tree/master))


## Folder description

```bash
├── docker
├── docker-compose.yml
├── docker-helper-images
├── docs
├── LICENSE
├── MANIFEST.in
├── mkdocs.yml
├── osmaxx
├── osmaxx/tests
└── README.md
```

* `docker`: docker specific setup. Currently only the dockerfile.
* `docker-compose.yml`: the (local) setup description to run docker containers in development
* `docker-helper-images`: All used docker images, that are used in this project, but are a bt othogonal
* `docs`: documentation
* `LICENSE`: MIT Licence for OSMaxx
* `MANIFEST.in`: Python description file (https://packaging.python.org/en/latest/guides/using-manifest-in/)
* `mkdocs.yml`: Documentation generator (https://www.mkdocs.org/)
* `osmaxx`: The source files of the osmaxx project
* `osmaxx/tests`: test for osmaxx
* `README.md`: The Readme, "standard" starting point for a OS project

## Development

[![Build Status](https://travis-ci.org/geometalab/osmaxx.svg?branch=develop)](https://travis-ci.org/geometalab/osmaxx) ([branch `develop`](https://github.com/geometalab/osmaxx/tree/develop))

* [development (with testing and setup instructions)](/docs/development/development.md)

The only supported way running this project is using docker containers.

## Production Deployment

FIXME: Describe the steps needed for production deployment

### Documentation

See [development (with testing and setup instructions)](/docs/development/development.md) for more details.
