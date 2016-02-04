# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('countries', '0002_inital_country_data_import'),
        ('conversion_job', '0003_auto_20151204_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='extent',
            name='country',
            field=models.ForeignKey(blank=True, null=True, to='countries.Country', verbose_name='country'),
        ),
    ]
