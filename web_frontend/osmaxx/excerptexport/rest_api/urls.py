from django.conf.urls import url

from osmaxx.countries import viewsets as country_viewsets
from . import views

urlpatterns = [
    url(r'^bounding_geometries/$', views.BoundingGeometryList.as_view()),
    url(r'^bounding_geometries/(?P<pk>[0-9]+)/$', views.BoundingGeometryDetail.as_view()),
    url(r'^bounding_geometry_from_excerpt/$', views.BoundingGeometryFromExcerptList.as_view()),
    url(r'^bounding_geometry_from_excerpt/(?P<pk>[0-9]+)/$', views.BoundingGeometryFromExcerptDetail.as_view()),
    url(r'^estimated_file_size/$', views.estimated_file_size),
    url(r'^bounding_geometry_from_excerpt/country-(?P<pk>[0-9]+)/$',
        country_viewsets.country_detail, name='country-detail'),
]
