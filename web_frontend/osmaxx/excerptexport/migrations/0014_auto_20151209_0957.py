# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0013_auto_20151207_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='extractionorder',
            name='country_id',
            field=models.IntegerField(blank=True, verbose_name='country ID', null=True),
        ),
        migrations.AlterField(
            model_name='extractionorder',
            name='excerpt',
            field=models.ForeignKey(related_name='extraction_orders', null=True, verbose_name='excerpt', to='excerptexport.Excerpt'),
        ),
    ]
