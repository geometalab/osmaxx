# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from osmaxx.countries.utils import get_polyfile_name_to_file_mapping, polyfile_to_geos_geometry


class Migration(migrations.Migration):
    def import_countries(apps, schema_editor):  # noqa
        tolerance = 0.01  # in degrees
        Country = apps.get_model("countries", "Country")  # noqa
        for name, polyfile_path in get_polyfile_name_to_file_mapping().items():
            geometry = polyfile_to_geos_geometry(polyfile_path)
            simplified_geometry = polyfile_to_geos_geometry(polyfile_path, simplify_tolerance=tolerance)
            Country.objects.create(
                name=name,
                polyfile=polyfile_path,
                polygon=geometry,
                simplified_polygon=simplified_geometry,
            )

    def remove_countries(apps, schema_editor):  # noqa
        Country = apps.get_model("countries", "Country")  # noqa
        Country.objects.all().delete()

    dependencies = [
        ('countries', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(import_countries, remove_countries),
    ]
