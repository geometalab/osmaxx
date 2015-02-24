# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BoundingBox',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('north', models.DecimalField(decimal_places=16, max_digits=16)),
                ('east', models.DecimalField(decimal_places=16, max_digits=16)),
                ('south', models.DecimalField(decimal_places=16, max_digits=16)),
                ('west', models.DecimalField(decimal_places=16, max_digits=16)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Excerpt',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=128)),
                ('is_public', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('bounding_box', models.OneToOneField(to='excerptExport.BoundingBox')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='excerpts')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExtractionOrder',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('state', models.IntegerField(default=1)),
                ('process_start_date', models.DateTimeField(verbose_name='process start date')),
                ('process_reference', models.CharField(max_length=128)),
                ('excerpt', models.ForeignKey(to='excerptExport.Excerpt', related_name='extraction_orders')),
                ('orderer', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='extraction_orders')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OutputFile',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('mime_type', models.CharField(max_length=64)),
                ('path', models.FileField(upload_to='', max_length=512)),
                ('create_date', models.DateTimeField(verbose_name='create date')),
                ('deleted_on_filesystem', models.BooleanField(default=False)),
                ('extraction_order', models.ForeignKey(to='excerptExport.ExtractionOrder', related_name='output_files')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
