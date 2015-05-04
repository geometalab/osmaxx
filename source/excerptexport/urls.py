from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout
from excerptexport.views import index, access_denied, new_excerpt_export, show_downloads, download_file, \
    create_excerpt_export, extraction_order_status


except_export_urlpatterns = patterns(
    '',
    url(r'^$', index, name='index'),
    url(r'^access_denied/$', access_denied, name='access_denied'),
    url(r'^new/$', new_excerpt_export, name='new'),
    url(r'^downloads/$', show_downloads, name='downloads'),
    url(r'^download/$', download_file, name='download'),
    url(r'^create/$', create_excerpt_export, name='create'),
    url(r'^orders/(?P<extraction_order_id>[0-9]+)$', extraction_order_status, name='status')
)

login_logout_patterns = patterns(
    '',
    url(r'^login/$', login,
        {'template_name': 'excerptexport/templates/login.html'}, name='login'),
    url(r'^logout/$', logout,
        {'template_name': 'excerptexport/templates/logout.html'}, name='logout'),
)

urlpatterns = except_export_urlpatterns + login_logout_patterns
