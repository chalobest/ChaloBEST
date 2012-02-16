from django.conf.urls.defaults import *
import settings
from os.path import join
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^chaloBEST/', include('chaloBEST.foo.urls')),
    url(r'^$','chaloBEST.views.index', name='index'),
    url(r'^static/(?P<path>.*)$','django.views.static.serve', {'document_root':'./static'}),
    (r'^routes/$', 'mumbai.views.routes'),
    (r'^route/(?P<alias>[a-zA-Z0-9\s\-]*?)/$', 'mumbai.views.route'),
    (r'^areas/$', 'mumbai.views.areas'),
    (r'^area/(?P<name>.*?)/$', 'mumbai.views.area'),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #(r'^grappelli/', include('grappelli.urls')),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

if settings.LOCAL_DEVELOPMENT:
#
  urlpatterns += patterns('',
#
  (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': join(settings.PROJECT_ROOT, "static")}),
#
)

