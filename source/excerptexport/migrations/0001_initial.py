# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import excerptexport.models.output_file
import django.contrib.gis.db.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BoundingGeometry',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BBoxBoundingGeometry',
            fields=[
                ('boundinggeometry_ptr', models.OneToOneField(
                    primary_key=True,
                    to='excerptexport.BoundingGeometry',
                    parent_link=True,
                    auto_created=True,
                    serialize=False
                )),
                ('south_west', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('north_east', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('type', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=('excerptexport.boundinggeometry',),
        ),
        migrations.CreateModel(
            name='Excerpt',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('is_public', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('bounding_geometry', models.OneToOneField(to='excerptexport.BoundingGeometry')),
                ('owner', models.ForeignKey(related_name='excerpts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExtractionOrder',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('state', models.IntegerField(default=1)),
                ('process_start_date', models.DateTimeField(verbose_name='process start date', null=True)),
                ('process_reference', models.CharField(blank=True, max_length=128, null=True)),
                ('excerpt', models.ForeignKey(related_name='extraction_orders', to='excerptexport.Excerpt')),
                ('orderer', models.ForeignKey(related_name='extraction_orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OutputFile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('mime_type', models.CharField(max_length=64)),
                ('file', models.FileField(blank=True, upload_to='/var/www/eda/projects/data', null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('deleted_on_filesystem', models.BooleanField(default=False)),
                ('public_identifier', models.CharField(
                    max_length=512,
                    default=excerptexport.models.output_file.default_public_identifier
                )),
                ('extraction_order', models.ForeignKey(
                    related_name='output_files',
                    to='excerptexport.ExtractionOrder'
                )),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
