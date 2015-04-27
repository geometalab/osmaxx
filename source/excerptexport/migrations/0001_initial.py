# -*- coding: utf-8 -*-
# don't check for validation errors in auto-generated migration file
# flake8: noqa
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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(default=0)),
                ('geometry', django.contrib.gis.db.models.fields.GeometryField(null=True, blank=True, srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Excerpt',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('is_public', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('bounding_geometry', models.OneToOneField(to='excerptexport.BoundingGeometry')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='excerpts')),
            ],
        ),
        migrations.CreateModel(
            name='ExtractionOrder',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('state', models.IntegerField(default=1)),
                ('process_start_date', models.DateTimeField(null=True, verbose_name='process start date')),
                ('process_reference', models.CharField(max_length=128, null=True, blank=True)),
                ('excerpt', models.ForeignKey(to='excerptexport.Excerpt', related_name='extraction_orders')),
                ('orderer', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='extraction_orders')),
            ],
        ),
        migrations.CreateModel(
            name='OutputFile',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('mime_type', models.CharField(max_length=64)),
                ('file', models.FileField(upload_to='/home/hsr/workspace/2015-Osmaxx/osmaxx/source/data', null=True, blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('deleted_on_filesystem', models.BooleanField(default=False)),
                ('public_identifier', models.UUIDField(default=uuid.uuid4)),
                ('extraction_order', models.ForeignKey(to='excerptexport.ExtractionOrder', related_name='output_files')),
            ],
        ),
    ]
