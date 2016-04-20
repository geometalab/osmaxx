from django.db import models
from django.utils.translation import ugettext_lazy as _
from rest_framework.reverse import reverse

from osmaxx.conversion_api.formats import FORMAT_CHOICES


class Export(models.Model):
    """
    Frontend-side representation of both, a export procedure in progress (or concluded) *and* the result of exporting.

    Each ``Export`` instance corresponds to a specific, individual ``job`` sent to the conversion service and thus
    encompasses

    - the spatial selection ('clipping' or 'extraction') of the input data within one perimeter
      (``extraction_order.excerpt`` or ``extraction_order.country_id`)
    - the transformation of the data from the data sources' schemata (e.g. ``osm2pgsql`` schema) to the OSMaxx schema
    - the actual export to one specific GIS or navigation file format with one specific set of parameters
    """
    extraction_order = models.ForeignKey('ExtractionOrder', related_name='exports',
                                         verbose_name=_('extraction order'))
    file_format = models.TextField(choices=FORMAT_CHOICES, verbose_name=_('file format / data format'))
    conversion_service_job_id = models.IntegerField(verbose_name=_('conversion service job ID'), null=True)

    def send_to_conversion_service(self, clipping_area_json, incoming_request):
        from osmaxx.api_client.conversion_api_client import ConversionApiClient
        api_client = ConversionApiClient()
        extraction_format = self.file_format
        gis_options = self.extraction_order.extraction_configuration['gis_options']
        parametrization_json = api_client.create_parametrization(clipping_area_json, extraction_format, gis_options)
        job_json = api_client.create_job(parametrization_json, self.status_update_url)
        self.conversion_service_job_id = job_json['id']
        self.save()
        return job_json

    def get_full_status_update_uri(self, request):
        return request.build_absolute_uri(self.status_update_url)

    @property
    def status_update_url(self):
        return reverse('job_progress:tracker', kwargs=dict(export_id=self.id))
