from django.conf.urls import include, url

urlpatterns = [
    # browsable REST API
    url(r'^api/', include('rest_api.urls')),
]
