# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0015_auto_20151211_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='extractionorder',
            name='process_start_time',
            field=models.DateTimeField(null=True, blank=True, verbose_name='process start time'),
        ),
    ]
