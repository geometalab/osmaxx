FROM debian:jessie

MAINTAINER geometalab <geometalab@hsr.ch>

RUN apt-get update && apt-get install -y \
  osmctools \
  wget \
  && rm -rf /var/lib/apt/lists/*

COPY ./update_pbf.sh /opt/update_pbf.sh

CMD /opt/update_pbf.sh
