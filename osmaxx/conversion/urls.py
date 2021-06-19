from rest_framework.routers import DefaultRouter

from osmaxx.clipping_area.viewsets import ClippingAreaViewSet
from osmaxx.conversion.viewsets import (
    JobViewSet,
    ParametrizationViewSet,
    FormatSizeEstimationView,
)
from pbf_file_size_estimation.views import SizeEstimationView

router = DefaultRouter()
router.register(
    r"estimate_size_in_bytes", SizeEstimationView, basename="estimate_size_in_bytes"
)
router.register(
    r"format_size_estimation",
    FormatSizeEstimationView,
    basename="format_size_estimation",
)
router.register(r"clipping_area", ClippingAreaViewSet, basename="clipping_area")
router.register(r"conversion_job", JobViewSet, basename="conversion_job")
router.register(
    r"conversion_parametrization",
    ParametrizationViewSet,
    basename="conversion_parametrization",
)

urlpatterns = router.urls
