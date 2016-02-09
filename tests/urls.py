from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from osmaxx.clipping_area.viewsets import ClippingAreaViewSet

router = DefaultRouter()
router.register(r'clipping_area', ClippingAreaViewSet, base_name='clipping_area')

urlpatterns = [
    url(r'^', include(router.urls)),
]
