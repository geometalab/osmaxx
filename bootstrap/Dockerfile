FROM geometalab/osm2pgsql

ENV USER data-wrangler
ENV HOME /home/$USER

RUN DEBIAN_FRONTEND=noninteractive apt-get update &&\
    DEBIAN_FRONTEND=noninteractive apt-get install -y\
    postgresql-client\
    osmosis\
    osmctools\
    wget

WORKDIR $HOME

WORKDIR $HOME/data-wrangler

COPY . $HOME/data-wrangler

CMD sh main-bootstrap.sh
