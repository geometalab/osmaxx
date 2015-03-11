# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('is_public', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='excerpts')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExtractionOrder',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('state', models.IntegerField(default=1)),
                ('process_start_date', models.DateTimeField(verbose_name='process start date')),
                ('process_reference', models.CharField(max_length=128)),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('mime_type', models.CharField(max_length=64)),
                ('path', models.CharField(max_length=512)),
                ('create_date', models.DateTimeField(verbose_name='create date')),
                ('deleted_on_filesystem', models.BooleanField(default=False)),
                ('extraction_order', models.ForeignKey(to='excerptexport.ExtractionOrder', related_name='output_files')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='boundinggeometry',
            name='excerpt',
            field=models.OneToOneField(to='excerptexport.Excerpt', null=True),
            preserve_default=True,
        ),
    ]
