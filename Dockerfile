FROM geometalab/python3-gis

ENV USER osmaxx

ENV COMPOSE_VERSION 1.3.1

RUN DEBIAN_FRONTEND=noninteractive apt-get update -q \
	&& DEBIAN_FRONTEND=noninteractive apt-get install -y -q --no-install-recommends curl ca-certificates \
	&& curl -o /usr/local/bin/docker-compose -L \
		"https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-Linux-x86_64" \
	&& chmod +x /usr/local/bin/docker-compose

ENV HOME /home/$USER

WORKDIR $HOME/source

COPY osmaxx-py $HOME/source

ENV REQS_LAST_UPDATED 22-06-2015 14:24

RUN pip3 install -Ur requirements/local.txt
