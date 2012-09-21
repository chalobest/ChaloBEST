from django.conf.urls.defaults import *
import settings
from os.path import join
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from feeds import RouteFeed
#import ox.django.api.urls
#import mumbai


urlpatterns = patterns('',
    # Example:
    # (r'^chaloBEST/', include('chaloBEST.foo.urls')),
#    url(r'^$','mumbai.views.index', name='index'),
    url(r'^$','views.index', name='index'),

    url(r'^about$', 'mumbai.views.about', name='about'),
    url(r'^android$', 'mumbai.views.android', name='android'),
    url(r'^contact$', 'mumbai.views.contact', name='contact'),
    url(r'^join_us$', 'mumbai.views.join_us', name='join_us'),
    url(r'^sms$', 'mumbai.views.sms', name='sms'),
    url(r'^stats/$','mumbai.views.stats', name='stats'),
#    url(r'^static/(?P<path>.*)$','django.views.static.serve', {'document_root':'./static'}),
    (r'^routes/$', 'mumbai.views.routes'),
    (r'^route/(?P<alias>[a-zA-Z0-9\s\-]*?)/$', 'mumbai.views.route'),
    (r'^route/(?P<alias>[a-zA-Z0-9\s\-]*?)/georss/$', RouteFeed()),
    (r'^areas/$', 'mumbai.views.areas'),
    (r'^area/(?P<name>.*?)/$', 'mumbai.views.area'),
#    (r'^area/(?P<name>.*?)/georss/$', AreaFeed()),
    (r'^stop/(?P<slug>.*?)/$', 'mumbai.views.stop'),
#    (r'^stop/(?P<slug>.*?)/georss/$', StopFeed()),
    (r'^buseditor/$', 'mumbai.views.buseditor'),	   
    (r'^editstops/$', 'mumbai.views.editstops'),
    #(r'^accounts/', include('allauth.urls')),
    (r'^1.0/', include('mumbai.apiurls')),
    (r'^route/freq/(?P<code>.*)$', 'mumbai.views.route_headway'), 
    #url(r'^login/', include('socialregistration.urls',namespace='socialregistration')),                                        
    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #(r'^grappelli/', include('grappelli.urls')),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^matchstops/$', 'mumbai.views.fuzzystops'),
    (r'^fuzzystops_edit/$', 'mumbai.views.fuzzystops_edit'),
 url(r'^accounts/', include('userena.urls')),
     #(r'^accounts/signup/$', 'userena.views.signup',
      #{'signup_form': SignupFormExtra}),

     url(r'^messages/',include('userena.contrib.umessages.urls')),

    
)

if settings.LOCAL_DEVELOPMENT:
#
  urlpatterns += patterns('',
#
  (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': join(settings.PROJECT_ROOT, "static")}),
  (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': join(settings.PROJECT_ROOT, "media")}),
#
)

