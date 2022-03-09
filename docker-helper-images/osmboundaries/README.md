# osm-boundaries
provides a database with the worldly polygons of water, land and coastlines from osmdata.

## usage

Assuming you have docker and docker-compose installed and set up, just run
the service.

When the import is done (on a machine with 8GB RAM and some SSD,
this process should be less than 10 Minutes), access the database in another
container through an attached network. How this is done can
be read at the docker-compsose user documentation.

The imported data is available in the three tables
`coastline_l`, `landmass_a`  and `sea_a`.

Currently the import is a one-time command, so that a docker-compsose up
should be sufficent to have the database filled and running.

If a docker-compsose up is run twice, the _old_ data in the database
is being overridden.

### Up

```bash
docker-compsose up
```

### Down

```bash
docker-compsose down
```

## development

### Obtain (or update) shapefiles

Since the shapefiles are not included in the sources,
run `./update_shapes.sh` to download their latest version.

### Build container from shapefiles in `data/` and test it

Run `docker-compose -f docker-compose.yml -f dev.yml build`
to build the new images using the shapefiles [just obtained](#obtain-or-update-shapefiles).

Run `docker-compose -f docker-compose.yml -f dev.yml up`.
If that doesn't cause any error messages,
use a psql-client to connect to `localhost` on port `5442`
with the username and password you used in the docker-compose file
and look at the data.

### Build and push the new shapes

Run `./build_and_push.sh` to build and push the latest image to dockerhub.
