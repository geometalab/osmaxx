# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversion_job', '0002_auto_20151119_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extent',
            name='polyfile',
            field=models.FileField(blank=True, null=True, verbose_name='polyfile (deprecated)', upload_to=''),
        ),
    ]
