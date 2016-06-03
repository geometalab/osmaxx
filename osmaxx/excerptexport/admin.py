from django.contrib import admin
from django.contrib.admin import widgets
from django.contrib.gis.db import models

from osmaxx.excerptexport.models import Excerpt, ExtractionOrder, OutputFile, Export


@admin.register(Excerpt)
class ExcerptAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.GeometryField: {'widget': widgets.AdminTextareaWidget}
    }
    list_display = ['name', 'is_public', 'is_active', 'owner']
    fields = ('name', ('bounding_geometry',), 'owner')
    list_per_page = 20
    search_fields = ['name', 'owner__username']
    list_filter = ['is_active', 'is_public', 'excerpt_type']


@admin.register(ExtractionOrder)
class ExtractionOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'excerpt', 'orderer', 'state')
    list_display_links = ('id', 'excerpt')
    readonly_fields = ('process_id', '_extraction_configuration', 'progress_url')

admin.site.register(OutputFile)

admin.site.register(Export)
