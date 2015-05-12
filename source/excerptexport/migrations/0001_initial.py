# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid
from django.conf import settings
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BoundingGeometry',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Excerpt',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(verbose_name='name', max_length=128)),
                ('is_public', models.BooleanField(default=False, verbose_name='is public')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
            ],
        ),
        migrations.CreateModel(
            name='ExtractionOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('state', models.IntegerField(default=1, verbose_name='state')),
                ('process_start_date', models.DateTimeField(null=True, verbose_name='process start date')),
                ('process_reference', models.CharField(blank=True, null=True, verbose_name='process reference', max_length=128)),
                ('excerpt', models.ForeignKey(to='excerptexport.Excerpt', verbose_name='excerpt', related_name='extraction_orders')),
                ('orderer', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='orderer', related_name='extraction_orders')),
            ],
        ),
        migrations.CreateModel(
            name='OutputFile',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('mime_type', models.CharField(verbose_name='mime type', max_length=64)),
                ('file', models.FileField(blank=True, upload_to='/var/www/eda/projects/data', null=True, verbose_name='file')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='create date')),
                ('deleted_on_filesystem', models.BooleanField(default=False, verbose_name='deleted on filesystem')),
                ('public_identifier', models.UUIDField(default=uuid.uuid4, verbose_name='public identifier')),
                ('extraction_order', models.ForeignKey(to='excerptexport.ExtractionOrder', verbose_name='extraction order', related_name='output_files')),
            ],
        ),
        migrations.CreateModel(
            name='BBoxBoundingGeometry',
            fields=[
                ('boundinggeometry_ptr', models.OneToOneField(to='excerptexport.BoundingGeometry', auto_created=True, parent_link=True, primary_key=True, serialize=False)),
                ('south_west', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('north_east', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
            bases=('excerptexport.boundinggeometry',),
        ),
        migrations.AddField(
            model_name='excerpt',
            name='bounding_geometry',
            field=models.OneToOneField(to='excerptexport.BoundingGeometry', verbose_name='bounding geometry'),
        ),
        migrations.AddField(
            model_name='excerpt',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='owner', related_name='excerpts'),
        ),
    ]
