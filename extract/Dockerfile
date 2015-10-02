# this gdal image comes with support for FileGDB
FROM geodata/gdal:2.0.0

# unfortunately, the image geodata/gdal used starts with the user 'nobody'
# so a switch is necessary first
USER root

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python\
    postgresql-client\
    zip

ENV HOME /home/excerpt

WORKDIR $HOME

ADD . $HOME

CMD python excerpt.py 8.775449276 47.1892350573 8.8901920319 47.2413633153 -f spatialite
