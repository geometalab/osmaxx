# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from countries.utils import get_polyfile_name_to_file_mapping, polyfile_to_GEOSGeometry


class Migration(migrations.Migration):
    def import_countries(apps, schema_editor):
        Country = apps.get_model("countries", "Country")
        for name, polyfile_path in get_polyfile_name_to_file_mapping().items():
            geometry = polyfile_to_GEOSGeometry(polyfile_path)
            Country.objects.create(
                name=name,
                polyfile=polyfile_path,
                associated_multipolygon=geometry,
            )

    def remove_countries(apps, schema_editor):
        Country = apps.get_model("countries", "Country")
        Country.objects.all().delete()

    dependencies = [
        ('countries', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(import_countries, remove_countries),
    ]
