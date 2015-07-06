FROM geometalab/python3-gis

ENV USER osmaxx
# ENV USERID 1000
# ENV GROUPID 1000
# RUN groupadd -g $GROUPID $USER && useradd -g $USERID --create-home --home-dir /home/$USER -g $USER $USER

ENV HOME /home/$USER

WORKDIR $HOME/source

COPY osmaxx-py $HOME/source

ENV REQS_LAST_UPDATED 22-06-2015 14:24

RUN pip3 install -Ur requirements/local.txt
