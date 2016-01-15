# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0007_auto_20151016_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='extractionorder',
            name='process_id',
            field=models.TextField(verbose_name='process link', blank=True, null=True, default=''),
        ),
    ]
