from django.conf.urls.defaults import *
import apiviews

urlpatterns = patterns('',
    (r'^route/(?P<alias>.*)$', apiviews.route), #FIXME: better regexp for route alias?
    (r'^stop/(?P<id>[0-9]*)$', apiviews.stop),
)
