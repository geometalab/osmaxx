FROM buildpack-deps:jessie

ENV USER osmaxx
ENV USERID 1000
ENV GROUPID 1000

RUN groupadd -g $GROUPID $USER && useradd -g $USERID --create-home --home-dir /home/$USER -g $USER $USER

ENV LANG en_US.utf8

EXPOSE 8000

# install geodjango dependencies: https://docs.djangoproject.com/en/1.8/ref/contrib/gis/install/geolibs/
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y\
    python3\
    python3-dev\
    binutils\
    libgeos-dev\
    libproj-dev\
    gdal-bin\
    libsqlite3-dev\
    libspatialite-dev\
    libgeoip1\
    gdal-bin\
    python-gdal\
    virtualenv

ENV HOME /home/$USER
ENV VIRTUALENV $HOME/.virtualenvs/$USER
ENV PIP $HOME/.virtualenvs/$USER/bin/pip
ENV ACTIVATE $HOME/.virtualenvs/$USER/bin/activate
ENV PYTHON $HOME/.virtualenvs/$USER/bin/python

ENV STATIC $HOME/static
ENV MEDIA $HOME/media
ENV PRIVATE_MEDIA $HOME/private_media

RUN chown -R $USER:$USER $HOME

#RUN mkdir $HOME/source && chown $USER:$USER $HOME/source
#RUN mkdir $HOME/static && chown $USER:$USER $HOME/static
#RUN mkdir $HOME/media && chown $USER:$USER $HOME/media
#RUN mkdir $HOME/private_media && chown $USER:$USER $HOME/private_media

# VOLUME $HOME/source
# VOLUME $HOME/static
# VOLUME $HOME/media
# VOLUME $HOME/private_media

USER $USER

WORKDIR $HOME/source


RUN virtualenv --system-site-packages --python=`which python3` $VIRTUALENV
RUN $PIP install -U setuptools
COPY requirements requirements
RUN $PIP install -r requirements/local.txt
