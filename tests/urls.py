from django.conf.urls import url, include
from osmaxx.conversion import urls as conversion_urls

urlpatterns = [
    url(r'^', include(conversion_urls)),
    url(r'^', include('osmaxx.excerptexport.urls', namespace='excerptexport')),
    url(r'^version/$', include('osmaxx.version.urls', namespace='version')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include('osmaxx.excerptexport.rest_api.urls', namespace='excerptexport_api')),
    url(r'^job_progress/', include('osmaxx.job_progress.urls', namespace='job_progress')),
    url(r'^pages/', include('osmaxx.core.urls', namespace='pages')),
]
