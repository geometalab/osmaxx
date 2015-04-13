# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.gis.db.models.fields
import excerptexport.models.output_file

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BoundingGeometry',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('type', models.IntegerField(default=0)),
                ('geometry', django.contrib.gis.db.models.fields.GeometryField(null=True, srid=4326, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Excerpt',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('is_public', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('bounding_geometry', models.OneToOneField(to='excerptexport.BoundingGeometry')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='excerpts')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExtractionOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('state', models.IntegerField(default=1)),
                ('process_start_date', models.DateTimeField(null=True, verbose_name='process start date')),
                ('process_reference', models.CharField(null=True, max_length=128, blank=True)),
                ('excerpt', models.ForeignKey(to='excerptexport.Excerpt', related_name='extraction_orders')),
                ('orderer', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='extraction_orders')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OutputFile',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('mime_type', models.CharField(max_length=64)),
                ('file', models.FileField(null=True, upload_to='/var/www/eda/projects/data', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('deleted_on_filesystem', models.BooleanField(default=False)),
                ('public_identifier', models.CharField(default=excerptexport.models.output_file.default_public_identifier, max_length=512)),
                ('extraction_order', models.ForeignKey(to='excerptexport.ExtractionOrder', related_name='output_files')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
