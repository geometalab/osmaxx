# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import osmaxx.excerptexport.utils.upload_to
import django.contrib.gis.db.models.fields
import uuid
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BoundingGeometry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
            ],
        ),
        migrations.CreateModel(
            name='Excerpt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='name', max_length=128)),
                ('is_public', models.BooleanField(verbose_name='is public', default=False)),
                ('is_active', models.BooleanField(verbose_name='is active', default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExtractionOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('state', models.IntegerField(verbose_name='state', default=1)),
                ('process_start_date', models.DateTimeField(verbose_name='process start date', null=True)),
                ('process_reference', models.CharField(verbose_name='process reference', blank=True, max_length=128, null=True)),
                ('excerpt', models.ForeignKey(verbose_name='excerpt', related_name='extraction_orders', to='excerptexport.Excerpt')),
                ('orderer', models.ForeignKey(verbose_name='orderer', related_name='extraction_orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OutputFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('mime_type', models.CharField(verbose_name='mime type', max_length=64)),
                ('file', models.FileField(verbose_name='file', blank=True, upload_to='', storage=osmaxx.excerptexport.utils.upload_to.PrivateFileSystemStorage(), null=True)),
                ('create_date', models.DateTimeField(verbose_name='create date', auto_now_add=True)),
                ('deleted_on_filesystem', models.BooleanField(verbose_name='deleted on filesystem', default=False)),
                ('public_identifier', models.UUIDField(verbose_name='public identifier', default=uuid.uuid4)),
                ('extraction_order', models.ForeignKey(verbose_name='extraction order', related_name='output_files', to='excerptexport.ExtractionOrder')),
            ],
        ),
        migrations.CreateModel(
            name='BBoxBoundingGeometry',
            fields=[
                ('boundinggeometry_ptr', models.OneToOneField(primary_key=True, serialize=False, parent_link=True, to='excerptexport.BoundingGeometry', auto_created=True)),
                ('south_west', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('north_east', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
            bases=('excerptexport.boundinggeometry',),
        ),
        migrations.AddField(
            model_name='excerpt',
            name='bounding_geometry',
            field=models.OneToOneField(verbose_name='bounding geometry', to='excerptexport.BoundingGeometry'),
        ),
        migrations.AddField(
            model_name='excerpt',
            name='owner',
            field=models.ForeignKey(verbose_name='owner', related_name='excerpts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='OsmosisPolygonFilterBoundingGeometry',
            fields=[
                ('boundinggeometry_ptr', models.OneToOneField(primary_key=True, serialize=False, parent_link=True, to='excerptexport.BoundingGeometry', auto_created=True)),
                ('polygon_file', models.FileField(storage=osmaxx.excerptexport.utils.upload_to.PrivateFileSystemStorage(), upload_to='')),
            ],
            bases=('excerptexport.boundinggeometry',),
        ),
    ]
