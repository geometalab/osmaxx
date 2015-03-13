EXPORT_OPTIONS = {
    'gis': {
        'name': 'GIS',
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
                'label': 'Coordinate reference system',
                'type': 'select',
                'select_multiple': False,
                'default': 'pseudomerkator',
                'groups': {
                    'global': {
                        'name': 'Global coordinate reference systems',
                        'values': {
                            'pseudomerkator': 'Pseudo merkator',
                            'wgs72': 'WGS 72',
                            'wgs84': 'WGS 84'
                        }
                    },
                    'utm': {
                        'name': 'UTM zones for your export',
                        'values': {
                            'utm32': 'UTM zone 32',
                            'utm33': 'UTM zone 33'
                        }
                    }
                }
            },
            'detail_level': {
                'label': 'Detail level',
                'type': 'radio',
                'default': 'verbatim',
                'values': {
                    'verbatim': 'Verbatim',
                    'simplified': 'Simplified',
                    'combined': 'Combined'
                }
            }
        }
    },
    'routing': {
        'name': 'Routing',
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
