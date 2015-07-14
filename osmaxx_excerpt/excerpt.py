import time, subprocess, os, argparse
import math
path = os.path.dirname(os.path.realpath(__file__))

def name_generator():
    filename='osmaxx_excerpt_'+time.strftime("%Y-%m-%d")+'_'+time.strftime("%H%M%S")
    return filename

def to_mercator(mercator_x_lon, mercator_y_lat):
    if math.fabs(mercator_x_lon) > 180 or math.fabs(mercator_y_lat) > 90:
        return
    num = mercator_x_lon * 0.017453292519943295
    x_value = 6378137.0 * num
    additional = mercator_y_lat * 0.017453292519943295
    mercator_x_lon = x_value
    mercator_y_lat = 3189068.5 * \
                     math.log((1.0 + math.sin(additional)) /
                              (1.0 - math.sin(additional)))
    return [mercator_x_lon, mercator_y_lat]

def get_statistics(data, name):
    statcmd = 'bash ./extract/extract_statistics '+data[0]+' '+data[1]+' '+data[2]+' '+data[3]+' '+name
    subprocess.check_call(statcmd, shell=True)


def call_fgdb(data, name):
    get_statistics(data, name)
    gdbcmd = 'sh ./extract/extract_fgdb.sh '+data[0]+' '+data[1]+' '+data[2]+' '+data[3]+' '+name
    subprocess.check_call(gdbcmd, shell=True)


def call_shp(data, name):
    get_statistics(data, name)
    shpcmd = 'sh ./extract/extract_shp.sh '+data[0]+' '+data[1]+' '+data[2]+' '+data[3]+' '+name
    subprocess.check_call(shpcmd, shell=True)


def call_gpkg(data, name):
    get_statistics(data, name)
    gpkgcmd = 'sh ./extract/extract_gpkg.sh '+data[0]+' '+data[1]+' '+data[2]+' '+data[3]+' '+name
    subprocess.check_call(gpkgcmd, shell=True)

def call_spatialite(data, name):
    get_statistics(data, name)
    spatialitecmd = 'sh ./extract/extract_spatialite.sh '+data[0]+' '+data[1]+' '+data[2]+' '+data[3]+' '+name
    subprocess.check_call(spatialitecmd, shell=True)


def call_test():
    xmin='8.775449276'
    ymin='47.1892350573'
    xmax='8.8901920319'
    ymax='47.2413633153'
    print 'Testing FileGDB Creation'
    myfile=name_generator()
    call_fgdb([xmin, ymin, xmax, ymax], myfile)
    print 'FileGDB have been created in '+path+'/data/'+myfile
    print 'Testing GPKG Creation'
    myfile=name_generator()
    call_gpkg([xmin, ymin, xmax, ymax], myfile)
    print 'GPPKG have been created in '+path+'/data/'+myfile
    print 'Testing ERSI ShapeFile Creation'
    myfile=name_generator()
    call_shp([xmin, ymin, xmax, ymax], myfile)
    print 'ERSI ShapeFile have been created in '+path+'/data/'+myfile
    print 'Testing Spatialite Creation'
    myfile=name_generator()
    call_shp([xmin, ymin, xmax, ymax], myfile)
    print 'Spatialite have been created in '+path+'/data/'+myfile

#call_test()

parser = argparse.ArgumentParser()
parser.add_argument('-f','--format',choices=['fgdb','shp','gpkg','spatialite'], default='fgdb', help= 'output formats')
parser.add_argument('xmin', help='Min Longitude/Left/West', type=float)
parser.add_argument('ymin', help='Min Latitude/Bottom/South', type=float)
parser.add_argument('xmax', help='Max Longitude/Right/East', type=float)
parser.add_argument('ymax', help='Max Latitude/Top/North', type=float)
args = parser.parse_args()
min_xy=to_mercator(args.xmin, args.ymin)
max_xy=to_mercator(args.xmax, args.ymax)
if args.format == 'fgdb':
	name=name_generator()
	call_fgdb([str(min_xy[0]), str(min_xy[1]), str(max_xy[0]), str(max_xy[1])], name)
	print name+' have been completed in FileGDB format'
elif args.format == 'shp':
	name=name_generator()
	call_shp([str(min_xy[0]), str(min_xy[1]), str(max_xy[0]), str(max_xy[1])], name)
	print name+' have been completed in ESRI Shapefile format'	
elif args.format == 'gpkg':
	name=name_generator()
	call_gpkg([str(min_xy[0]), str(min_xy[1]), str(max_xy[0]), str(max_xy[1])], name)
	print name+' have been completed in GPKG format'
elif args.format == 'spatialite':
	name=name_generator()
	call_spatialite([str(min_xy[0]), str(min_xy[1]), str(max_xy[0]), str(max_xy[1])], name)
	print name+' have been completed in Spatialite format'


