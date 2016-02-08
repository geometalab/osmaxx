# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from osmaxx.countries.utils import get_polyfile_name_to_file_mapping, polyfile_to_geos_geometry

too_large_polyfiles = [
    'Argentina',
    'Austria',
    'Brazil',
    'China',
    'Czech Republic',
    'France',
    'Germany',
    'India',
    'Mexico',
    'Russian Federation',
    'South Africa',
    'United States of America',
]


class Migration(migrations.Migration):
    def remove_too_large_countries(apps, schema_editor):  # noqa
        Country = apps.get_model("countries", "Country")  # noqa
        for country_name in too_large_polyfiles:
            Country.objects.filter(name=country_name).delete()

    def import_countries(apps, schema_editor):  # noqa
        tolerance = 0.01  # in degrees
        Country = apps.get_model("countries", "Country")  # noqa
        poly_file_mapping = get_polyfile_name_to_file_mapping()
        for country_name in too_large_polyfiles:
            Country.objects.filter(name=country_name).delete()
            geometry = polyfile_to_geos_geometry(poly_file_mapping[country_name], simplify_tolerance=tolerance)
            Country.objects.create(
                name=country_name,
                polyfile=poly_file_mapping[country_name],
                simplified_polygon=geometry,
            )

    dependencies = [
        ('countries', '0002_inital_country_data_import'),
    ]

    operations = [
        migrations.RunPython(remove_too_large_countries, import_countries),
    ]
