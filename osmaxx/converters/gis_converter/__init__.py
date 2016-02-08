from osmaxx.converters import Options

options = Options(
    output_formats=['fgdb', 'shp', 'gpkg', 'spatialite'],
)

__all__ = [
    'options',
]
