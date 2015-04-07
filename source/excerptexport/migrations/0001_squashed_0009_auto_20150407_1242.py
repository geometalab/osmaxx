# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.gis.db.models.fields
import excerptexport.models.output_file


def revert_one_to_one_bounding_geo_to_excerpt(apps, schema_editor):
    Excerpt = apps.get_model('excerptexport', 'Excerpt')
    for excerpt in Excerpt.objects.all():
        excerpt.bounding_geometry = excerpt.boundinggeometry
        excerpt.save()

def revert_one_to_one_excerpt_to_bounding_geo(apps, schema_editor):
    BoundingGeometry = apps.get_model('excerptexport', 'BoundingGeometry')
    for bounding_geometry in BoundingGeometry.objects.all():
        bounding_geometry.excerpt_old = bounding_geometry.excerpt
        bounding_geometry.save()

class Migration(migrations.Migration):

    replaces = [('excerptexport', '0001_initial'), ('excerptexport', '0002_auto_20150320_1421'), ('excerptexport', '0002_auto_20150317_1330'), ('excerptexport', '0003_merge'), ('excerptexport', '0004_auto_20150324_1637'), ('excerptexport', '0005_auto_20150407_1115'), ('excerptexport', '0006_excerpt_bounding_geometry'), ('excerptexport', '0007_auto_20150407_1117'), ('excerptexport', '0008_remove_boundinggeometry_excerpt_old'), ('excerptexport', '0009_auto_20150407_1242')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BoundingGeometry',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(default=0)),
                ('geometry', django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Excerpt',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('mime_type', models.CharField(max_length=64)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('deleted_on_filesystem', models.BooleanField(default=False)),
                ('extraction_order', models.ForeignKey(to='excerptexport.ExtractionOrder', related_name='output_files')),
                ('file', models.FileField(blank=True, null=True, upload_to='/var/www/eda/projects/data')),
                ('public_identifier', models.CharField(max_length=512, default=excerptexport.models.output_file.default_public_identifier)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='boundinggeometry',
            name='excerpt_old',
            field=models.OneToOneField(to='excerptexport.Excerpt', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='extractionorder',
            name='process_reference',
            field=models.CharField(max_length=128, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='extractionorder',
            name='process_reference',
            field=models.CharField(max_length=128, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='extractionorder',
            name='process_start_date',
            field=models.DateTimeField(verbose_name='process start date', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='extractionorder',
            name='process_reference',
            field=models.CharField(max_length=128, blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='excerpt',
            name='bounding_geometry',
            field=models.OneToOneField(to='excerptexport.BoundingGeometry', null=True),
            preserve_default=True,
        ),
        migrations.RunPython(
            code=revert_one_to_one_bounding_geo_to_excerpt,
            reverse_code=revert_one_to_one_excerpt_to_bounding_geo,
            atomic=True,
        ),
        migrations.RemoveField(
            model_name='boundinggeometry',
            name='excerpt_old',
        ),
        migrations.AlterField(
            model_name='excerpt',
            name='bounding_geometry',
            field=models.OneToOneField(to='excerptexport.BoundingGeometry', default=None),
            preserve_default=False,
        ),
    ]
