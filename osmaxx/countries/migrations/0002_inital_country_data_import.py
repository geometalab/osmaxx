# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    def import_countries(apps, schema_editor):  # noqa
        # no import should happen anymore in new installations
        pass

    def remove_countries(apps, schema_editor):  # noqa
        Country = apps.get_model("countries", "Country")  # noqa
        Country.objects.all().delete()

    dependencies = [
        ('countries', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(import_countries, remove_countries),
    ]
