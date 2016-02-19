from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from osmaxx.countries.viewsets import CountryViewSet

router = DefaultRouter()
router.register(r'country', CountryViewSet, base_name='country'),

urlpatterns = [
    url(r'', include(router.urls)),
]
