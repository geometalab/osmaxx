from django.contrib import admin
from django.utils.safestring import mark_safe

from osmaxx.excerptexport.models import Excerpt, ExtractionOrder, OutputFile, Export


@admin.register(Excerpt)
class ExcerptAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_public', 'is_active', 'owner', 'bounding_geometry']
    fields = ('name', ('bounding_geometry',))

    def bounding_geometry_subclass_instance_edit_link(self, excerpt):
        admin_link = excerpt.bounding_geometry.subclass_instance.get_admin_url()
        return mark_safe(
            '<a href="{}">'
            '<img src="/static/admin/img/icon_changelink.gif" alt="Change" height="10" width="10"></img> Edit {} {}'
            '</a>'.format(
                admin_link,
                type(excerpt.bounding_geometry.subclass_instance).__name__,
                excerpt.bounding_geometry.subclass_instance.id,
            ),
        )
    bounding_geometry_subclass_instance_edit_link.short_description = 'Boundary'


@admin.register(ExtractionOrder)
class ExtractionOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'excerpt', 'orderer', 'state')
    list_display_links = ('id', 'excerpt')
    readonly_fields = ('process_id', '_extraction_configuration', 'progress_url')

admin.site.register(OutputFile)

admin.site.register(Export)
