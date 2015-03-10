# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excerptExport', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoundingGeometry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('north', models.DecimalField(decimal_places=8, max_digits=12)),
                ('east', models.DecimalField(decimal_places=8, max_digits=12)),
                ('south', models.DecimalField(decimal_places=8, max_digits=12)),
                ('west', models.DecimalField(decimal_places=8, max_digits=12)),
                ('type', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='excerpt',
            name='bounding_box',
            field=models.OneToOneField(to='excerptExport.BoundingGeometry'),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='BoundingBox',
        ),
    ]
