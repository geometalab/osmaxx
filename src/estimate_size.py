#!/usr/bin/env python

import csv
import sys
import os
import math

if len(sys.argv) != 6:
	print('Usage: ' + os.path.basename(__file__) + ' infile.csv minlon minlat maxlon maxlat')
	sys.exit(2)

# read command line arguments
f = open(sys.argv[1], 'rb') # open the csv file
minlonbbox = float(sys.argv[2])
minlatbbox = float(sys.argv[3])
maxlonbbox = float(sys.argv[4])
maxlatbbox = float(sys.argv[5])

if minlonbbox >= maxlonbbox:
	print('ERROR: maxlon must be greater than minlon')
	sys.exit(2)

if minlatbbox >= maxlatbbox:
	print('ERROR: maxlat must be greater than minlat')
	sys.exit(2)

if (minlonbbox < -180 or minlonbbox > 180):
	print('ERROR: minlon out of range')
	sys.exit(2)

if (minlatbbox < -90 or minlatbbox > 90):
	print('ERROR: minlat out of range')
	sys.exit(2)

if (maxlonbbox < -180 or maxlonbbox > 180):
	print('ERROR: maxlon out of range')
	sys.exit(2)

if (maxlatbbox < -90 or maxlatbbox > 90):
	print('ERROR: maxlat out of range')
	sys.exit(2)

size = {} # according to http://stackoverflow.com/a/6696418
try:
	reader = csv.reader(f) # create the reader object
	for row in reader:     # iterate the rows of the file in orders
		lat = str(row[0]) # cast to string in order to use as key in associative array
		lon = str(row[1])
		size[lat, lon] = int(row[2])
finally:
	f.close() # close the csv file

# convert degrees to radians
def deg2rad(deg):
	return math.pi*deg/180

# calculate the ratio (area covered by bbox / area of the bbox extended to 1 degree grid boundaries)
# pre-conditions:
# - minlonbbox <= maxlonbbox
# - minlatbbox <= maxlatbbox
def ratio(minlonbbox, minlatbbox, maxlonbbox, maxlatbbox):
	
	# increase bbox by rounding outwards to the grid size
	minlongrid = math.floor(minlonbbox)
	minlatgrid = math.floor(minlatbbox)
	maxlongrid = math.ceil(maxlonbbox)
	maxlatgrid = math.ceil(maxlatbbox)

	# see https://gis.stackexchange.com/questions/59087/how-to-calculate-the-size-a-bounding-box (see also comment by user 'whuber')
	part  = (maxlonbbox-minlonbbox) * (math.sin(deg2rad(maxlatbbox))-math.sin(deg2rad(minlatbbox)))
	whole = (maxlongrid-minlongrid) * (math.sin(deg2rad(maxlatgrid))-math.sin(deg2rad(minlatgrid)))

	return part/whole

# increase bbox by rounding outwards to the grid size
minlongrid = math.floor(minlonbbox)
minlatgrid = math.floor(minlatbbox)
maxlongrid = math.ceil(maxlonbbox)
maxlatgrid = math.ceil(maxlatbbox)

# main loop: iterate over all tiles that are partially or fully covered by the bbox
estimated_size = int(0)
for mylat in range(int(minlatgrid), int(maxlatgrid)):
	for mylon in range(int(minlongrid), int(maxlongrid)):
		estimated_size += size[str(mylat), str(mylon)] * ratio(max(mylon,minlonbbox), max(mylat,minlatbbox), min(mylon+1,maxlonbbox), min(mylat+1,maxlatbbox))
		
print(int(round(estimated_size)))


