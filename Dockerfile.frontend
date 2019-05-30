# This GDAL image comes with support for FileGDB and has Python 3.6 already installed.
# Based on image _/ubuntu.

FROM geometalab/gdal-docker:v3.0.0

USER root

ENV PYTHONUNBUFFERED=non-empty-string PYTHONIOENCODING=utf-8 LC_ALL=C.UTF-8 LANG=C.UTF-8
ENV DJANGO_OSMAXX_CONVERSION_SERVICE_USERNAME=default_user DJANGO_OSMAXX_CONVERSION_SERVICE_PASSWORD=default_password
ENV NUM_WORKERS=5 DATABASE_HOST=frontenddatabase DATABASE_PORT=5432 APP_PORT=8000 APP_HOST=0.0.0.0

RUN DEBIAN_FRONTEND=noninteractive apt-get clean \
    && DEBIAN_FRONTEND=noninteractive apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    git \
    libpq-dev

# Install required Python packages:
ENV USER py
ENV HOME /home/$USER
WORKDIR $HOME

RUN pip3 install honcho
ADD ./requirements.txt $HOME/requirements.txt
RUN pip3 install -r requirements.txt

# TODO: this is just a temporary solution, use pip for production as soon as geometalab.osmaxx is published there
ADD ./ $HOME

RUN mkdir -p $HOME/docker_entrypoint/osmaxx/web_frontend $HOME/entrypoint
COPY ./docker_entrypoint/osmaxx/web_frontend $HOME/entrypoint
COPY ./docker_entrypoint/wait-for-it/wait-for-it.sh $HOME/entrypoint/wait-for-it.sh

EXPOSE 8000

ENTRYPOINT ["/home/py/entrypoint/entrypoint.sh"]
CMD ["honcho", "-f", "./web_frontend/Procfile.django.prod", "start"]
