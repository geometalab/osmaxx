from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from osmaxx.clipping_area.viewsets import ClippingAreaViewSet
from osmaxx.conversion.viewsets import JobViewSet, ParametrizationViewSet
from pbf_file_size_estimation.views import SizeEstimationView

router = DefaultRouter()
router.register(r'estimate_size_in_bytes', SizeEstimationView, base_name='estimate_size_in_bytes')
router.register(r'clipping_area', ClippingAreaViewSet, base_name='clipping_area')
router.register(r'conversion_job', JobViewSet, base_name='conversion_job')
router.register(r'conversion_parametrization', ParametrizationViewSet, base_name='conversion_parametrization')

urlpatterns = [
    url(r'^', include(router.urls)),
]
