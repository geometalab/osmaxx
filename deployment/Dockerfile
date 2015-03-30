FROM debian:jessie

MAINTAINER Tobias Blaser <tblaser@hsr.ch>

RUN mkdir /scripts
ADD setupSoftware.sh /setup
ADD setupDatabaseAndGeoExtensions.sh /setup

CMD ["/bin/bash"]
