FROM debian:jessie

ENV REFRESHED_AT 2015-05-18

ENV LANG en_US.utf8

# get the nginx package and set it up
RUN ["apt-get", "update"]
RUN ["apt-get", "-y", "install", "nginx"]

# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log
RUN ln -sf /dev/stderr /var/log/nginx/error.log
VOLUME ["/var/cache/nginx"]
EXPOSE 80 443

# load nginx conf
ADD ./site.conf /etc/nginx/sites-available/osmaxx
RUN ["ln", "-s", "/etc/nginx/sites-available/osmaxx", "/etc/nginx/sites-enabled/osmaxx"]
RUN ["rm", "-rf", "/etc/nginx/sites-available/default"]

#start the server
CMD ["nginx", "-g", "daemon off;"]
