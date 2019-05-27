FROM ubuntu:18.04

MAINTAINER geometalab <geometalab@hsr.ch>

RUN apt-get update && apt-get install -y \
  osmctools \
  wget \
  python3 \
  python3-pip \
  && rm -rf /var/lib/apt/lists/*

RUN pip3 install sentry-sdk

COPY ./pbf_updater.py /opt/pbf_updater.py
COPY ./delvelopment_download_only.sh /opt/delvelopment_download_only.sh

ENTRYPOINT /opt/pbf_updater.py

# default wait between updates is one hour, in seconds
CMD "--wait-seconds" ${wait_seconds:-3600}
