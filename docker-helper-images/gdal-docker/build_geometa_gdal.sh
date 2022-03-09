#!/bin/bash

set -e

# https://gdal.org/download.html#current-releases
GDAL_VERSION="3.4.1"
PROJ_VERSION="8.2.1"

# if not cloned already, clone it:
git clone git@github.com:OSGeo/gdal.git gdal || true

cd gdal/docker

git pull

# python:3 -> 08.2021 = bullseye (debian)
WITH_PDFIUM=1 WITH_FILEGDB=1 BASE_IMAGE="ubuntu:20.04" TARGET_BASE_IMAGE="ubuntu:20.04" TARGET_IMAGE="geometalab/gdal:full" ubuntu-full/build.sh --release --gdal v${GDAL_VERSION} --proj ${PROJ_VERSION}
# WITH_FILEGDB=1 BASE_IMAGE="python:3" TARGET_BASE_IMAGE="python:3" TARGET_IMAGE="geometalab/gdal:full" ubuntu-full/build.sh --release --gdal v${GDAL_VERSION} --proj ${PROJ_VERSION}
# WITH_PDFIUM=1 WITH_FILEGDB=1 BASE_IMAGE="python:3" TARGET_BASE_IMAGE="python:3" TARGET_IMAGE="geometalab/gdal:full" ubuntu-full/build.sh --release --gdal v${GDAL_VERSION}
# WITH_PDFIUM=0 WITH_FILEGDB=1 BASE_IMAGE="ubuntu:21.04" TARGET_IMAGE="geometalab/gdal:${GDAL_VERSION}" ubuntu-full/build.sh --release --gdal v${GDAL_VERSION} --proj ${PROJ_VERSION}

docker push "geometalab/gdal:full-v${GDAL_VERSION}"

docker run --rm -it "geometalab/gdal:full-v${GDAL_VERSION}" ogrinfo --formats | grep -i gdb
