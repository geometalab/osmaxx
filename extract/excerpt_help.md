# excerpt.py documentation

## functions

1. name_generator- generates the name of the db depending on the date and time
2. to_mercator- converts the map projection of the default osm format to the mercator projection
3. get_statistics- calls the extract_statistics.sh with the coordinates which calculates the statistics for csv file
4. call_db- calls the required shell script for conversion to the said data format
5. Main function- Creates variables with coordinates and the data format. After that, call the to_mercator function and then call the shell script.
