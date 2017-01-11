from django.contrib import admin
from django.contrib.admin import widgets
from django.contrib.gis.db import models

from osmaxx.excerptexport.models import Excerpt, ExtractionOrder, OutputFile, Export


@admin.register(Excerpt)
class ExcerptAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.GeometryField: {'widget': widgets.AdminTextareaWidget}
    }
    list_display = ['name', 'is_active', 'excerpt_type', 'is_public', 'owner']
    fields = (('name', 'excerpt_type'), 'is_active', ('bounding_geometry',), 'is_public', 'owner')
    list_per_page = 20
    search_fields = ['name', 'owner__username']
    list_filter = ['is_active', 'is_public', 'excerpt_type']


@admin.register(ExtractionOrder)
class ExtractionOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'excerpt', 'orderer')
    list_display_links = ('id', 'excerpt')
    readonly_fields = ('process_id', 'coordinate_reference_system', 'progress_url')


@admin.register(OutputFile)
class OutputFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'mime_type', 'file', 'creation_date', 'file_removal_at')
    list_display_links = ('id', )
    list_filter = ['file_removal_at']
    fields = ['mime_type', 'file']
    readonly_fields = ['creation_date', 'file_removal_at']


@admin.register(Export)
class ExportAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_format', 'conversion_service_job_id', 'status', 'finished_at')
    list_display_links = ('id', )
    list_filter = ['finished_at', 'created_at', 'updated_at']
    fields = ('file_format', 'conversion_service_job_id', 'status', 'finished_at', 'created_at', 'updated_at')
    readonly_fields = ('finished_at', 'created_at', 'updated_at')
