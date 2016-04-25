from __future__ import unicode_literals

from django.db import migrations


def set_export_fk_from_extraction_order_and_content_type(apps, schema_editor):
    OutputFile = apps.get_model('excerptexport', 'OutputFile')  # noqa
    for output_file in OutputFile.objects.all():
        output_file.export = output_file.extraction_order.exports.get(file_format=output_file.content_type)
        output_file.save()


def set_extraction_order_fk_and_content_type_from_export(apps, schema_editor):
    OutputFile = apps.get_model('excerptexport', 'OutputFile')  # noqa
    for output_file in OutputFile.objects.all():
        output_file.extraction_order = output_file.export.extraction_order
        output_file.content_type = output_file.export.file_format
        output_file.save()


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0022_outputfile_export'),
    ]

    operations = [
        migrations.RunPython(
            set_export_fk_from_extraction_order_and_content_type,
            set_extraction_order_fk_and_content_type_from_export
        )
    ]
