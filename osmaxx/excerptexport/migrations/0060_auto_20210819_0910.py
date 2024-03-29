# Generated by Django 3.2.6 on 2021-08-19 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0059_auto_20170712_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='excerpt',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='export',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='extractionorder',
            name='coordinate_reference_system',
            field=models.IntegerField(choices=[(4326, 'WGS 84'), (3857, 'Pseudo-Mercator'), (4322, 'WGS 72'), (4269, 'NAD 83'), (4277, 'OSGB 36')], default=4326, verbose_name='CRS'),
        ),
        migrations.AlterField(
            model_name='extractionorder',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='outputfile',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
