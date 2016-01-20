FROM geometalab/python3-gis

ENV USER osmaxx

ENV HOME /home/$USER

WORKDIR $HOME

# if you update your requirements, please update this to the actual date/time, 
# otherwise docker uses the cache from the intermediate image build (not re-running pip3).
ENV REQS_LAST_UPDATED 16-12-2015 10:47

ADD web_frontend/requirements $HOME/requirements

RUN pip3 install -r requirements/local.txt

WORKDIR $HOME/source

COPY web_frontend $HOME/source

ADD ./entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
