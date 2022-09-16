# Generated by Django 3.2.6 on 2021-08-19 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0005_auto_20170511_1100'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='permission',
            options={'ordering': ['content_type__app_label', 'content_type__model', 'codename'], 'verbose_name': 'permission', 'verbose_name_plural': 'permissions'},
        ),
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(max_length=150, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
    ]