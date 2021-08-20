#!/bin/bash
set -e

cd $(dirname $0)
./update_shapes.sh

docker build -t geometalab/osmboundaries:latest .
docker push geometalab/osmboundaries:latest
