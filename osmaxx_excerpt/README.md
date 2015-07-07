# Extract Osmaxx Map
This contains the extraction of Osmaxx map

Using:  
python excerpt.py xmin ymin xmax ymax -f [format]  

Options:  
    xmin: Min Longitude/Left/West  
    ymin: Min Latitude/Bottom/South  
    xmax: Max Longitude/Right/East  
    ymax: Max Latitude/Top/North  
    -f {fgdb,shp,gpkg,spatialite}, --format {fgdb,shp,gpkg,spatialite}  

Examples:  
python excerpt.py 36.7035198212 -1.344585964 36.8252277374 -1.2577477129 -f gpkg  
python excerpt.py 8.775449276 47.1892350573 8.8901920319 47.2413633153 -f shp  
python excerpt.py 8.8 47.20 8.9 47.26 -f spatialite  
python excerpt.py 8.8 47.20 8.9 47.26 -f fgdb  
python excerpt.py 8.8 47.20 8.9 47.26  
