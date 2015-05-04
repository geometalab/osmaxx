from django.conf.urls import patterns, url


urlpatterns = patterns(
    'excerptexport.views',
    url(r'^$', 'index', name='index'),
    url(r'^access_denied/$', 'access_denied', name='access_denied'),
    url(r'^new/$', 'new_excerpt_export', name='new'),
    url(r'^downloads/$', 'show_downloads', name='downloads'),
    url(r'^download/$', 'download_file', name='download'),
    url(r'^create/$', 'create_excerpt_export', name='create'),
    url(r'^orders/(?P<extraction_order_id>[0-9]+)$', 'extraction_order_status', name='status')
)

urlpatterns += patterns(
    '',
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'excerptexport/templates/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'template_name': 'excerptexport/templates/logout.html'}, name='logout'),
)
