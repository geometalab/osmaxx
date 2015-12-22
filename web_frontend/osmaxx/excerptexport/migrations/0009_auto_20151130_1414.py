# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0008_extractionorder_process_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extractionorder',
            name='process_id',
            field=models.TextField(null=True, blank=True, verbose_name='process link'),
        ),
    ]
