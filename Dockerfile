FROM buildpack-deps:jessie

ENV USER osmaxx
# ENV USERID 1000
# ENV GROUPID 1000

# RUN groupadd -g $GROUPID $USER && useradd -g $USERID --create-home --home-dir /home/$USER -g $USER $USER

ENV LANG en_US.utf8

# All ENV vars should be written here, and default to production settings.
# They can be overridden using docker-compose for development/testing.

# EMAIL
ENV DJANGO_DEFAULT_FROM_EMAIL='noreply osmaxx <noreply@osmaxx.hsr.ch>'

# DATABASE
ENV DJANGO_ALLOWED_HOSTS='[".osmaxx.hsr.ch.",]'

# SSL
# set this to 60 seconds and then to 518400 when you can prove it works
ENV DJANGO_SECURE_HSTS_SECONDS=60
ENV DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=true
ENV DJANGO_SECURE_SSL_REDIRECT=true
ENV DJANGO_SECURE_SSL_HOST='osmaxx.hsr.ch'
ENV DJANGO_SECURE_REDIRECT_EXEMPT=[]

# OTHER SECURITY SETTINGS
ENV DJANGO_SECURE_CONTENT_TYPE_NOSNIFF=true
ENV DJANGO_SECURE_BROWSER_XSS_FILTER=true
ENV DJANGO_SESSION_COOKIE_SECURE=true
ENV DJANGO_SESSION_COOKIE_HTTPONLY=true
ENV DJANGO_CSRF_COOKIE_SECURE=true
ENV DJANGO_CSRF_COOKIE_HTTPONLY=true
ENV DJANGO_X_FRAME_OPTIONS='DENY'

# install geodjango dependencies: https://docs.djangoproject.com/en/1.8/ref/contrib/gis/install/geolibs/
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y\
    python3\
    python3-pip\
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

WORKDIR $HOME/source

RUN pip3 install -U pip
RUN pip3 install -U honcho

COPY osmaxx-py $HOME/source

ENV REQS_LAST_UPDATED 22-06-2015 14:24

RUN pip3 install -Ur requirements/local.txt
