import time

from django_rq import job

from converters import osm_cutter
from converters.gis_converter.bootstrap import bootstrap
from converters.gis_converter.extract.excerpt import Excerpt
from converters.osm_cutter import GEOMETRY_CLASSES_ACTION, BBox


@job
def convert(geometry, format_options, output_directory=None):
    """
    Starts converting an excerpt for the specified format options

    :param geometry: osm_cutter.BBox or TBD
    :param format_type_options: TBD
    :param output_directory: where results are being stored
        uses '/tmp/' + time.strftime("%Y-%m-%d_%H%M%S") for default
    :return: resulting paths/urls for created file
    """

    # sanity check of input param
    klass = geometry.__class__
    if klass not in GEOMETRY_CLASSES_ACTION:
        raise NotImplementedError(klass.__name__ + ' has not been implemented yet')

    if not output_directory:
        output_directory = '/tmp/' + time.strftime("%Y-%m-%d_%H%M%S")

    pbf_path = osm_cutter.cut_osm_extent(geometry)
    bootstrap.boostrap(pbf_path)

    # strip trailing slash
    if output_directory[-1] == '/':
        output_directory = output_directory[:-1]

    formats = format_options['formats']
    excerpt = Excerpt(formats=formats, output_dir=output_directory)
    excerpt.start()


if __name__ == '__main__':
    geometry = BBox(29.525547623634335, 40.77546776498174, 29.528980851173397, 40.77739734768811)
    format_options = {
        'formats': ['fgdb', 'spatialite', 'shp', 'gpkg']
    }
    convert(geometry=geometry, format_options=format_options)
