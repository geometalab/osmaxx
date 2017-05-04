from django.conf.urls import include, url

urlpatterns = [
    # browsable REST API
    url(r'^api/', include('osmaxx.rest_api.urls')),
    url(r'^version/', include('osmaxx.version.urls', namespace='version')),
]
