from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^bounding_geometries/$', views.BoundingGeometryList.as_view()),
    url(r'^bounding_geometries/(?P<pk>[0-9]+)/$', views.BoundingGeometryDetail.as_view()),
]
