from django.conf import settings
from django.conf.urls import include
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin

from osmaxx.excerptexport.urls import excerpt_export_urlpatterns
from osmaxx.core.urls import pages_patterns
from osmaxx.profile.urls import profile_patterns

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("version/", include("osmaxx.version.urls", namespace="version")),
        # browsable REST API
        path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
        path(
            "api/",
            include(
                "osmaxx.excerptexport.rest_api.urls", namespace="excerptexport_api"
            ),
        ),
        path("pages/", include(pages_patterns)),
        path("profile/", include(profile_patterns)),
        path("", include(excerpt_export_urlpatterns)),
        path("", include("social_django.urls", namespace="social")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes=True)
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
