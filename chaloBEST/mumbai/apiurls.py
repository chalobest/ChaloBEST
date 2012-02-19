from django.conf.urls.defaults import *
import apiviews

urlpatterns = patterns('',
    (r'^route/(?P<code>[0-9]*)$', apiviews.route),
)
