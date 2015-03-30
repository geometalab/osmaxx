#!/bin/bash

echo "[setup] configure database ..."
sudo -u postgres psql -c "CREATE USER osmaxx WITH PASSWORD 'osmaxx';"
sudo -u postgres psql -c "CREATE DATABASE osmaxx ENCODING 'UTF8';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE osmaxx TO osmaxx;"
echo "------------ available databases ------------"
sudo -u postgres psql -c "SELECT datname FROM pg_database WHERE datistemplate = false;"
echo "---------------------------------------------"

echo "[setup] install & configure geodata extensions ..."
sudo apt-get -y install binutils libgeos-3.4. # GEOS
sudo apt-get -y install libproj0 # PROJ.4
sudo apt-get -y install python-gdal # GDAL
sudo apt-get -y install postgis
sudo -u postgres psql -c "CREATE EXTENSION postgis;" "osmaxx"
sudo -u postgres psql -c "CREATE EXTENSION postgis_topology;" "osmaxx"
