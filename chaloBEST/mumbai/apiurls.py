from django.conf.urls.defaults import *
import apiviews

urlpatterns = patterns('',
    (r'^route/(?P<code>.*)$', apiviews.route), #FIXME: better regexp for route alias?
    (r'^area/(?P<slug>.*)$', apiviews.area),
    (r'^stop/(?P<slug>.*)$', apiviews.stop),
    (r'^routes/$', apiviews.routes),
    (r'^areas/$', apiviews.areas),
    (r'^stops/$', apiviews.stops),
    (r'^stops_near/$', apiviews.stops_near),
)


#    (r'route/freq/(?P<code>.*)$', views.route_headway), 
