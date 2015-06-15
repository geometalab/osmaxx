FROM buildpack-deps:jessie
ENV REFRESHED_AT 2015-05-18
ENV LANG en_US.utf8

ENV USER osmaxx
ENV USERID 1000
ENV GROUPID 1000

RUN groupadd -g $GROUPID $USER && useradd -g $USERID --create-home --home-dir /home/$USER -g $USER $USER


ENV STATIC $HOME/static
ENV MEDIA $HOME/media
ENV PRIVATE_MEDIA $HOME/private_media

RUN mkdir -p $STATIC
RUN mkdir -p $MEDIA
RUN mkdir -p $PRIVATE_MEDIA

RUN chown -R $USER:$USER $HOME

USER $USER

#VOLUME $STATIC
#VOLUME $MEDIA
#VOLUME $PRIVATE_MEDIA

ENV HOME /home/osmaxx
WORKDIR /home/osmaxx
