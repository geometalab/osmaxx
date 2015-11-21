FROM geometalab/python3-gis

ENV USER osmaxx

ENV HOME /home/$USER

WORKDIR $HOME

# if you update your requirements, please update this to the actual date/time, 
# otherwise docker uses the cache from the intermediate image build (not re-running pip3).
ENV REQS_LAST_UPDATED 18-11-2015 08:28

ADD osmaxx-py/requirements $HOME/requirements

RUN pip3 install -r requirements/local.txt

WORKDIR $HOME/source

COPY osmaxx-py $HOME/source
