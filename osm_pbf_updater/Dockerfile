FROM debian:jessie

MAINTAINER geometalab <geometalab@hsr.ch>

RUN apt-get update && apt-get install -y \
  osmctools \
  wget \
  python3 \
  && rm -rf /var/lib/apt/lists/*

COPY ./pbf_updater.py /opt/pbf_updater.py

ENTRYPOINT /opt/pbf_updater.py

# default wait between updates is one hour, in seconds
CMD "--wait-seconds" ${wait_seconds:-3600}
