FROM debian:jessie
ENV REFRESHED_AT 2015-05-18
ENV LANG en_US.utf8
# move into our working directory
RUN ["groupadd", "osmaxx"]
RUN ["useradd", "osmaxx", "-s", "/bin/bash", "-m", "-g", "osmaxx", "-G", "osmaxx"]
ENV HOME /home/osmaxx
WORKDIR /home/osmaxx
# ADD must be after chown see http://stackoverflow.com/a/26145444/1281947
RUN ["chown", "-R", "osmaxx:osmaxx", "/home/osmaxx"]
USER osmaxx
