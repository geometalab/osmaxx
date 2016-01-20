# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0002_auto_20150729_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extractionorder',
            name='_extraction_configuration',
            field=models.TextField(blank=True, null=True, verbose_name='extraction options', default=''),
        ),
    ]
