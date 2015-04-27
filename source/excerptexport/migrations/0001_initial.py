# -*- coding: utf-8 -*-
# don't check for validation errors in auto-generated migration file
# flake8: noqa
from __future__ import unicode_literals

from django.db import models, migrations
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('type', models.IntegerField(default=0)),
                ('geometry', django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Excerpt',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=128)),
                ('is_public', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('bounding_geometry', models.OneToOneField(to='excerptexport.BoundingGeometry')),
                ('owner', models.ForeignKey(related_name='excerpts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExtractionOrder',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('state', models.IntegerField(default=1)),
                ('process_start_date', models.DateTimeField(null=True, verbose_name='process start date')),
                ('process_reference', models.CharField(max_length=128, blank=True, null=True)),
                ('excerpt', models.ForeignKey(related_name='extraction_orders', to='excerptexport.Excerpt')),
                ('orderer', models.ForeignKey(related_name='extraction_orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OutputFile',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('public_identifier', models.UUIDField(auto_created=True)),
                ('mime_type', models.CharField(max_length=64)),
                ('file', models.FileField(blank=True, null=True, upload_to='/home/hsr/workspace/2015-Osmaxx/osmaxx/source/data')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('deleted_on_filesystem', models.BooleanField(default=False)),
                ('extraction_order', models.ForeignKey(related_name='output_files', to='excerptexport.ExtractionOrder')),
            ],
        ),
    ]
