import csv
import math

from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError


class OutOfBoundsError(ValidationError):
    pass


def estimate_size_of_extent(csv_source_file, west, south, east, north):
    if south >= north:
        raise OutOfBoundsError(_('north must be greater than south'))

    if west < -180 or west > 180:
        raise OutOfBoundsError(_('west out of range'))

    if south < -90 or south > 90:
        raise OutOfBoundsError(_('south out of range'))

    if east < -180 or east > 180:
        raise OutOfBoundsError(_('east out of range'))

    if north < -90 or north > 90:
        raise OutOfBoundsError(_('north out of range'))

    size_dict = _get_size_from_csv(csv_source_file)
    if west >= east:
        # we need to add it twice: from west to -180 and east to 180
        # from -180 to east
        size = _estimate_size(west=-180, south=south, east=east, north=north, size_dict=size_dict)
        # from west to 180
        size += _estimate_size(west=west, south=south, east=180, north=north, size_dict=size_dict)
        return size

    return _estimate_size(west=west, south=south, east=east, north=north, size_dict=size_dict)


def _get_size_from_csv(csv_source_file):
    size = {}  # according to http://stackoverflow.com/a/6696418
    with open(csv_source_file, 'r') as csv_file:
        try:
            reader = csv.reader(csv_file)
            for row in reader:
                lat = str(row[0])  # cast to string in order to use as key in associative array
                lon = str(row[1])
                size[lat, lon] = int(row[2])
        finally:
            csv_file.close()
    return size


def _estimate_size(west, south, east, north, size_dict):
    # increase bbox by rounding outwards to the grid size
    minlongrid = math.floor(west)
    minlatgrid = math.floor(south)
    maxlongrid = math.ceil(east)
    maxlatgrid = math.ceil(north)

    # main loop: iterate over all tiles that are partially or fully covered by the bbox
    estimated_size = int(0)
    for mylat in range(int(minlatgrid), int(maxlatgrid)):
        for mylon in range(int(minlongrid), int(maxlongrid)):
            ratio_value = _ratio(
                max(mylon, west),
                max(mylat, south),
                min(mylon + 1, east),
                min(mylat + 1, north)
            )
            size_value = size_dict[str(mylat), str(mylon)]
            estimated_size += size_value * ratio_value
    return int(round(estimated_size))


# convert degrees to radians
def _deg2rad(deg):
    return math.pi * deg / 180


# calculate the ratio (area covered by bbox / area of the bbox extended to 1 degree grid boundaries)
# pre-conditions:
# - minlonbbox <= maxlonbbox
# - minlatbbox <= maxlatbbox
def _ratio(minlonbbox, minlatbbox, maxlonbbox, maxlatbbox):
    # increase bbox by rounding outwards to the grid size
    minlongrid = math.floor(minlonbbox)
    minlatgrid = math.floor(minlatbbox)
    maxlongrid = math.ceil(maxlonbbox)
    maxlatgrid = math.ceil(maxlatbbox)

    # see https://gis.stackexchange.com/questions/59087/how-to-calculate-the-size-a-bounding-box (see also comment by user 'whuber')
    part = (maxlonbbox - minlonbbox) * (math.sin(_deg2rad(maxlatbbox)) - math.sin(_deg2rad(minlatbbox)))
    whole = (maxlongrid - minlongrid) * (math.sin(_deg2rad(maxlatgrid)) - math.sin(_deg2rad(minlatgrid)))

    return part / whole


__all__ = [
    'estimate_size_of_extent',
]
