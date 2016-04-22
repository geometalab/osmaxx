FROM python:3

RUN apt-get update && apt-get install -y git \
 autotools-dev libjpeg-dev libtiff5-dev libpng-dev libgif-dev libxt-dev libfreetype6-dev autoconf automake libtool libltdl7-dev libxml2-dev libuninameslist-dev libspiro-dev python-dev libpango1.0-dev libcairo2-dev \
 automake \
 unifont

WORKDIR /home/fontforge

RUN git clone https://github.com/fontforge/libspiro.git
WORKDIR /home/fontforge/libspiro
RUN autoreconf -i && automake --foreign -Wall && ./configure && make && make install

WORKDIR /home/fontforge

RUN git clone https://github.com/fontforge/libuninameslist.git
WORKDIR /home/fontforge/libuninameslist
RUN autoreconf -i && automake --foreign && ./configure && make && make install

WORKDIR /home/fontforge

RUN git clone https://github.com/fontforge/fontforge.git
WORKDIR /home/fontforge/fontforge
RUN ./bootstrap && PYTHON=python3 ./configure --enable-pyextension && make && make install && ldconfig

WORKDIR /home/fontforge

WORKDIR /home/fonts
ADD ./requirements.txt /requirements.txt

RUN pip3 install -U ipython pip
RUN pip3 install -r /requirements.txt

ADD ./creator.py /home/fontforge/creator.py
ADD ./osmaxx_v1_definition.yml /home/fontforge/osmaxx_v1_definition.yml

WORKDIR /home/fontforge