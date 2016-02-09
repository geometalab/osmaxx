from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

import osmaxx.conversion_job.views
from osmaxx.clipping_area.viewsets import ClippingAreaViewSet
from osmaxx.countries.views import CountryViewSet

router = DefaultRouter()
router.register(r'extents', osmaxx.conversion_job.views.ExtentViewSet)
router.register(r'jobs', osmaxx.conversion_job.views.ConversionJobViewSet)
router.register(r'conversion_result', osmaxx.conversion_job.views.ConversionJobStatusViewSet, base_name='conversion_job_result')
router.register(r'gis_format', osmaxx.conversion_job.views.GISFormatStatusViewSet)
router.register(r'country', CountryViewSet)
router.register(r'clipping_area', ClippingAreaViewSet, base_name='clipping_area')

urlpatterns = [
    url(r'^', include(router.urls)),
]
