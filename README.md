# Osmaxx

Short project name for "<strong>O</strong>pen<strong>S</strong>treet<strong>M</strong>ap <strong>a</strong>rbitrary e<strong>x</strong>cerpt e<strong>x</strong>port".

Cuts out OpenStreetMap data, processes it to geodata and converts it to typical GIS fileformats before being prepared for download. 

Website: http://osmaxx.hsr.ch/

## Development

See https://github.com/geometalab/osmaxx-docs for documentations and `/docs/development.md` for 
more detailed instructions.

## Run it locally on Linux

### Prerequisites

To run this project locally, you need docker and docker-compose installed 
(https://docs.docker.com/installation/ubuntulinux/ and https://docs.docker.com/compose/install/).

### Initialization/Docker container bootstrapping

To setup all the containers and their dependencies, run

`python manage_docker.py bootstrap`

### Running the project

Start the conatainers using docker compose:

`docker-compose up`

or

`python manage_docker.py run`

# Documentation

See Wiki: https://github.com/geometalab/osmaxx/wiki
