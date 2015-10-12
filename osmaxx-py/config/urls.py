from django.conf.urls import include, url
from django.contrib import admin

from social.apps.django_app import urls as social_urls

from osmaxx.excerptexport import urls as excerptexport_urls
from version.urls import version_urls

urlpatterns = [
    url(r'', include(excerptexport_urls, namespace='excerptexport')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include(social_urls, namespace='social')),
    url(r'^version/$', include(version_urls, namespace='version')),
    # browsable REST API
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include('osmaxx.excerptexport.rest_api.urls', namespace='excerptexport_api')),
]
