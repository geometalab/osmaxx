EXPORT_OPTIONS = {
    'gis': {
        'formats': {
            'file_gdb': {
                'name': 'FileGDB',
                'file_extension': 'gdb'
            },
            'geo_package': {
                'name': 'GeoPackage',
                'file_extension': 'geo'
            },
            'shape_file': {
                'name': 'ShapeFile',
                'file_extension': 'shape'
            }
        },
        'options': {
            'coordinate_reference_system': {
                'type': 'select',
                'select_multiple': False,
                'groups': {
                    'global': {
                        'name': 'Global coordinate reference systems',
                        'values': [
                            { 'key': 'pseudomerkator', 'name': 'Pseudo merkator' },
                            { 'key': 'wgs72', 'name': 'WGS 72' },
                            { 'key': 'wgs84', 'name': 'WGS 84' }
                        ]
                    },
                    'utm': {
                        'name': 'UTM zones for your export',
                        'values': [
                            { 'key': 'utm32', 'name': 'UTM zone 32' },
                            { 'key': 'utm33', 'name': 'UTM zone 33' }
                        ]
                    }
                }
            },
            'detail_level': {
                'type': 'radio',
                'values': [
                    { 'key': 'verbatim', 'name': 'Verbatim' },
                    { 'key': 'simplified', 'name': 'Simplified' },
                    { 'key': 'combined', 'name': 'Combined' }
                ]
            }
        }
    },
    'routing': {
        'formats': {
            'img': {
                'name': 'IMG',
                'file_extension': 'img'
            }
        },
        'options': {

        }
    }
}
