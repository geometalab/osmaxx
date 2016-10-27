#!/bin/bash
set -e

nice="nice -n 19"
osm_planet_base_dir="/var/data/osm-planet"
pbf_dir="${osm_planet_base_dir}/pbf"
osm_planet_mirror="${osm_planet_mirror:-http://ftp.gwdg.de/pub/misc/openstreetmap/planet.openstreetmap.org}"
osm_planet_path_relative_to_mirror="${osm_planet_path_relative_to_mirror:-/pbf/planet-latest.osm.pbf}"
complete_planet_mirror_url="${osm_planet_mirror}${osm_planet_path_relative_to_mirror}"
planet_latest="${pbf_dir}/planet-latest.osm.pbf"
planet_latest_on_update="${pbf_dir}/new_planet-latest.osm.pbf"
planet_diff="${pbf_dir}/planet-latest.osc.gz"

initial_download() {
  mkdir -p ${pbf_dir}
  ${nice} wget --continue -O ${planet_latest}_tmp ${complete_planet_mirror_url}
  ${nice} mv ${planet_latest}_tmp ${planet_latest}
}

update() {
  # all steps are idempotent, they can be repeated without information loss/duplication
  ${nice} osmupdate -v ${osmupdate_extra_params} ${planet_latest} ${planet_latest_on_update} || true
  if [ -f "${planet_latest_on_update}" ]; then
    ${nice} mv ${planet_latest_on_update} ${planet_latest}
  fi
}

if [ ! -f "${planet_latest}" ]; then
  initial_download
fi

while [ 1 ]
do
  update
  sleep 10
done
