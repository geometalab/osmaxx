# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extractionorder',
            name='process_reference',
            field=models.CharField(null=True, max_length=128),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='extractionorder',
            name='process_start_date',
            field=models.DateTimeField(verbose_name='process start date', null=True),
            preserve_default=True,
        ),
    ]
