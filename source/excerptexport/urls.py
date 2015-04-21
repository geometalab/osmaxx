from django.conf.urls import patterns, url

from excerptexport import views


urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),

    url('^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'excerptexport/templates/login.html'}, name='login'),
    url('^logout/$', 'django.contrib.auth.views.logout',
        {'template_name': 'excerptexport/templates/logout.html'}, name='logout'),

    url(r'^new/$', views.new_excerpt_export, name='new'),

    url(r'^downloads/$', views.show_downloads, name='downloads'),
    url(r'^download/$', views.download_file, name='download'),

    url(r'^create/$', views.create_excerpt_export, name='create'),

    url(r'^orders/(?P<extraction_order_id>[0-9]+)$', views.extraction_order_status, name='status')
)
