# https://djangosnippets.org/snippets/10428/

import math

UTM_NORTHERN_BASE = 32600
UTM_SOUTHERN_BASE = 32700

DEFAULT_MAP_SRID = 4326


def get_utm_zone(point):
    """
    Guess the UTM zone ID for the supplied point
    """
    # hardcode the target reference system:
    # this is WGS84 by spec
    wgspoint = point.transform("WGS84", clone=True)
    # remember, geographers are sideways
    lon = wgspoint.x
    return int(1 + (lon + 180.0) / 6.0)


def is_utm_northern(point):
    """
    Determine if the supplied point is in the northern or southern part
    for the UTM coordinate system.
    """
    wgspoint = point.transform("WGS84", clone=True)
    lat = wgspoint.y
    return lat >= 0.0


def get_utm_srid(point):
    """
    Given the input point, guess the UTM zone and hemissphere and
    return the SRID for the UTM appropriate UTM zone.

    Note that this does not do any range checking, so supplying bogus
    points yields undefined results.
    """
    utm_zone = get_utm_zone(point)
    is_northern = is_utm_northern(point)
    if is_northern:
        return UTM_NORTHERN_BASE + utm_zone
    else:
        return UTM_SOUTHERN_BASE + utm_zone


def buffer_from_meters(geom, buffer_meters):
    """
    Create a buffer around the supplied geometry
    with the specified distance.

    This is a wrapper around GEOMSGeometry.buffer()
    but with the buffer distance specified in meters.

    GEOM should be in the coordinate system the map will be drawn in,
    this is usually "web mercator", i.e. EPSG:3857
    """
    # The buffer calculation needs to happen in the source
    # coordinate system, otherwise stretching occurs
    # (e.g. circles become more and more egg-like further away from the equator)
    #
    # At the same time we want distances in meters to be
    # as close to correct as possible given the local environment.
    #
    # The approach taken here is
    # (1) use the centroid of the input geometry to determine a single reference
    #     point
    # (2) transform this reference point into the appropriate UTM coordinate system
    #     This is done using the correct UTM zone for the reference put.
    #     to keep differences to a minimum.
    # (3) shift the UTM version of the reference point to the north and east
    #     by buffer_meters / sqrt(2).
    # (4) transform the shifted point back from UTM to the input coordinate system
    #     and calculate the distance between the shifted point and the original point
    #     in the input coordinate system.
    # (5) Use this newly obtain distance value to create
    #     a buffered geometry from the original.

    ref_point = geom.centroid.clone()
    if not ref_point.srid:
        # default to WGS84
        ref_point.srid = 4326

    utm_srid = get_utm_srid(ref_point)
    utm_point = ref_point.transform(utm_srid, clone=True)

    shift_distance = buffer_meters / math.sqrt(2.0)
    shifted_point = utm_point.clone()
    shifted_point.x = shifted_point.x + shift_distance
    shifted_point.y = shifted_point.y + shift_distance

    shifted_ref = shifted_point.transform(ref_point.srid, clone=True)

    distance = shifted_ref.distance(ref_point)
    return distance


def with_metric_buffer(geom, buffer_meters, map_srid=DEFAULT_MAP_SRID):
    """
    Create a buffer around geom of the specified
    size.

    BUFFER_METERS is the size of the geometry buffer in meters.
    This is calculated regardless of the input coordinate system.

    MAP_SRID is the coordinate system for the map display.
    This defaults to DEFAULT_MAP_SRID, i.e. web mercator, EPSG:3857.
    The buffer is actually created in this coordinate system
    so that geometric figures (circles) are preserved as
    much as possible in the display.

    For example, creating a buffer around a point object
    results in a polygon that will largely resemble a circle
    on the map even if it is clearly elliptical in real coordinates.
    """
    if not geom.srid:
        geom = geom.clone()
        geom.srid = 4326

    if map_srid:
        map_geom = geom.transform(map_srid, clone=True)
    else:
        map_geom = geom
    buf_size = buffer_from_meters(map_geom, buffer_meters)
    buffered_geom = map_geom.buffer(buf_size)
    buffered_geom.transform(geom.srid)
    return buffered_geom
