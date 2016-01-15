# Osmaxx
Short project name for "<strong>O</strong>pen<strong>S</strong>treet<strong>M</strong>ap <strong>a</strong>rbitrary e<strong>x</strong>cerpt e<strong>x</strong>port".

Cuts out OpenStreetMap data, processes it to geodata and converts it to typical GIS fileformats before being prepared for download. 

Website: http://osmaxx.hsr.ch/

## Development
See https://github.com/geometalab/osmaxx-docs for documentations and `/docs/development.md` for instructions.


## Run it locally on Linux

**Setup**

To run this project locally, you need docker and docker-compose installed 
(https://docs.docker.com/installation/ubuntulinux/ and https://docs.docker.com/compose/install/).

Then run 

`./setup-containers.sh`

**Running the project**

From now on you can start the project using docker compose:

`docker-compose up webapp`

**running things inside the container**

`docker-compose run webapp <command>`

For example, to run tests, you can use:

`docker-compose run webapp python3 manage.py test`


### Useful Docker commands

Save docker image to file:
```shell
docker save osmaxx_database > /tmp/osmaxx-database-alpha1.docker-img.tar
docker save osmaxx_webapp > /tmp/osmaxx-webapp-alpha1.docker-img.tar
```

Load docker image from file:
```shell
docker load < /tmp/osmaxx-database-alpha1.docker-img.tar
docker load < /tmp/osmaxx-database-alpha1.docker-img.tar
```


# Documentation

See Wiki: https://github.com/geometalab/osmaxx/wiki
