EXPORT_OPTIONS = {
    'gis': {
        'name': 'GIS',
        'formats': {
            'file_gdb': {
                'name': 'FileGDB',
                'file_extension': 'gdb',
                'mime_type': 'application/octet-stream'
            },
            'geo_package': {
                'name': 'GeoPackage',
                'file_extension': 'geo',  # ???
                'mime_type': 'application/octet-stream'  # Not verified!
            },
            'shape_file': {
                'name': 'ShapeFile',
                'file_extension': 'shp',
                'mime_type': 'application/octet-stream'  # Not verified!
            }
        },
        'options': {
            'coordinate_reference_system': {
                'label': 'Coordinate reference system',
                'type': 'select',
                'select_multiple': False,
                'default': 'pseudomerkator',
                'groups': [
                    {
                        'name': 'Global coordinate reference systems',
                        'values': [
                            { 'name': 'pseudomerkator', 'label': 'Pseudo merkator' },
                            { 'name': 'wgs72', 'label': 'WGS 72' },
                            { 'name': 'wgs84', 'label': 'WGS 84' }
                        ]
                    },
                    {
                        'name': 'UTM zones for your export',
                        'values': [
                            { 'name': 'utm32', 'label': 'UTM zone 32' },
                            { 'name': 'utm33', 'label': 'UTM zone 33' }
                        ]
                    }
                ]
            },
            'detail_level': {
                'label': 'Detail level',
                'type': 'radio',
                'default': 'verbatim',
                'values': [
                    { 'name': 'verbatim', 'label': 'Verbatim' },
                    { 'name': 'simplified', 'label': 'Simplified' }
                ]
            }
        }
    },
    'routing': {
        'name': 'Routing',
        'formats': {
            'img': {
                'name': 'IMG (Garmin)',
                'file_extension': 'img',
                'mime_type': 'application/octet-stream'  # Not verified!
            }
        },
        'options': {

        }
    }
}
