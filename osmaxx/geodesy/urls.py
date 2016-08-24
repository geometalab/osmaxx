from rest_framework.routers import DefaultRouter

from osmaxx.geodesy.views import UTMZonesForGeometryViewSet

router = DefaultRouter()
router.register(r'utm_zones', UTMZonesForGeometryViewSet, base_name='utm_zones')
urlpatterns = router.urls
