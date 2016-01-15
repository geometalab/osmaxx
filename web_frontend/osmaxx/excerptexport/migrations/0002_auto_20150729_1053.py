# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extractionorder',
            name='process_reference',
        ),
        migrations.AddField(
            model_name='extractionorder',
            name='_extraction_configuration',
            field=models.TextField(blank=True, verbose_name='extraction options', null=True),
        ),
    ]
