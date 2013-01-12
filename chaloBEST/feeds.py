#from django.contrib.syndication.views import Feed
#from django.contrib.gis.feeds import Feed
from django.contrib.gis.feeds import Feed
from mumbai.models import *
from django.shortcuts import get_object_or_404




class RouteFeed(Feed):
#    description_template = 'feeds/route_description.html'
    
    def get_object(self, request, code):
        return get_object_or_404(Route, code=code)
        
    def title(self, obj):
        return "ChaloBEST.in: Feed for Bus No.: %s" % obj.display_name

    def description(self, obj):
        return "GeoRSS Route Feed"

    def geometry(self, obj):
        return obj.from_stop.point

    def link(self, obj):
        return obj.get_absolute_url()

    def items(self, obj):
        return Stop.objects.filter(routedetail__route=obj)

    def item_title(self, obj):
        return obj.display_name

    def item_geometry(self, obj):
        return obj.point
        
    def item_link(self, obj):
        return obj.get_absolute_url()

    def item_description(self, obj):
        return obj.display_name #FIXME
