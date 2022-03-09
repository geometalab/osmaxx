#!/usr/bin/env bash
set -ex

if [[ -f "/var/data/osm-planet/pbf/planet-latest.osm.pbf" ]]; then
  echo "PBF has already been assembled"
  exit 0
fi

mkdir -p /var/data/osm-planet/pbf

wget -O /tmp/monaco-latest.osm.pbf http://download.geofabrik.de/europe/monaco-latest.osm.pbf

wget -O /tmp/switzerland-latest.osm.pbf http://download.geofabrik.de/europe/switzerland-latest.osm.pbf

osmconvert /tmp/monaco-latest.osm.pbf -o=/tmp/monaco-latest.osm
osmconvert /tmp/switzerland-latest.osm.pbf -o=/tmp/switzerland-latest.osm
osmconvert /tmp/monaco-latest.osm /tmp/switzerland-latest.osm -o=/var/data/osm-planet/pbf/planet-latest.osm.pbf

rm -f /tmp/monaco-latest.osm /tmp/switzerland-latest.osm /tmp/monaco-latest.osm.pbf /tmp/switzerland-latest.osm.pbf
# for world tests:
# wget --continue -nv --show-progress --progress=bar:force:noscroll --tries=20 --read-timeout=20 -O planet-latest.osm.pbf https://ftp.gwdg.de/pub/misc/openstreetmap/planet.openstreetmap.org/pbf/planet-latest.osm.pbf
