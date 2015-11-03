import os

from conversion_service.converters.converter_settings import OSMAXX_CONVERSION_SERVICE


def cut_osm_extent(geometry_defintion):
    workdir_osm = OSMAXX_CONVERSION_SERVICE.get('WORKDIR')
    output_filename = os.path.join(workdir_osm, 'excerpt.osm.pbf')
    os.makedirs(workdir_osm, exist_ok=True)
    return geometry_defintion.cut_pbf(output_filename=output_filename)

__all__ = [
    'cut_osm_extent',
]
