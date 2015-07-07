FROM geometalab/osm2pgsql

ENV USER data-wrangler
ENV HOME /home/$USER

RUN DEBIAN_FRONTEND=noninteractive apt-get update &&\
    DEBIAN_FRONTEND=noninteractive apt-get install -y\
    postgresql-client\
    osmosis\
    wget

WORKDIR $HOME

WORKDIR $HOME/data-wrangler

COPY . $HOME/data-wrangler

COPY switzerland-latest.osm.pbf /tmp/osmosis/switzerland-latest.osm.pbf

CMD sh main-bootstrap.sh
