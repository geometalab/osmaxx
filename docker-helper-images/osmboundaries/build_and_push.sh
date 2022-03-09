#!/bin/bash
set -e

cd $(dirname $0)

docker build -t geometalab/osmboundaries:latest .
docker push geometalab/osmboundaries:latest
