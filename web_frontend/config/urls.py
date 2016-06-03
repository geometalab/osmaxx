from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'', include('osmaxx.excerptexport.urls', namespace='excerptexport')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^version/', include('osmaxx.version.urls', namespace='version')),
    # browsable REST API
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include('osmaxx.excerptexport.rest_api.urls', namespace='excerptexport_api')),
    url(r'^job_progress/', include('osmaxx.job_progress.urls', namespace='job_progress')),
    url(r'^pages/', include('osmaxx.core.urls', namespace='pages')),
] + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True) + \
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes=True)
