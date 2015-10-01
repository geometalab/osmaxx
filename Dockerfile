FROM geometalab/python3-gis

ENV USER osmaxx

ENV COMPOSE_VERSION 1.3.3

RUN DEBIAN_FRONTEND=noninteractive apt-get update -q \
	&& DEBIAN_FRONTEND=noninteractive apt-get install -y -q --no-install-recommends curl ca-certificates \
	&& curl -o /usr/local/bin/docker-compose -L \
		"https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-Linux-x86_64" \
	&& chmod +x /usr/local/bin/docker-compose

ENV HOME /home/$USER

WORKDIR $HOME

# if you update your requirements, please update this to the actual date/time, 
# otherwise docker uses the cache from the intermediate image build (not re-running pip3).
ENV REQS_LAST_UPDATED 30-09-2015 11:48

ADD osmaxx-py/requirements $HOME/requirements

RUN pip3 install -r requirements/local.txt

WORKDIR $HOME/source

COPY osmaxx-py $HOME/source
