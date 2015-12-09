from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^bounding_geometries/$', views.BoundingGeometryList.as_view()),
    url(r'^bounding_geometries/(?P<pk>[0-9]+)/$', views.BoundingGeometryDetail.as_view()),
    url(r'^bounding_geometry_from_excerpt/$', views.BoundingGeometryFromExcerptList.as_view()),
    url(r'^bounding_geometry_from_excerpt/(?P<pk>[0-9]+)/$', views.BoundingGeometryFromExcerptDetail.as_view()),
    url(r'^bounding_geometry_from_excerpt/country-(?P<pk>[0-9]+)/$', views.country_geojson),
]
