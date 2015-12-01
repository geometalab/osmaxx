# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0009_auto_20151130_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='extractionorder',
            name='progress_url',
            field=models.URLField(null=True, verbose_name='progress URL', blank=True),
        ),
    ]
