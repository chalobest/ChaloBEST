from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
import json
from os.path import join
from gtfs.gtfs_export import *

def index(request):
    return render_to_response('index.html', {} )


def stats(request):
    #No. of stops left
    
    total_stops = Stop.objects.count()
    stops_left = total_stops
    for stp in Stop.objects.all():
        if stp.point:
            stops_left-=1
    
        
    #list of of areas having stops left
    arealist = Area.objects.all()

    area_stat = []

    for area in arealist:
 #       area_stops = area.stop_set.all()
 #       astops_left = len(area_stops)
        astops_left = Stop.objects.filter(area=area).filter(point=None).count()
#        for stp in area_stops:
#            if stp.point:
#                astops_left-=1 
#       
        area_stat.append({'area':area,'neededstops':astops_left})
   
    

    #Routes having min stops left...
    route_stats_temp = getRoutesHavingSomeLocs(5)
    route_stat = []
    for routedict in route_stats_temp:
        if routedict['neededstops']:
            route_stat.append(routedict)
    ret = {}
    ret['area_stat'] = area_stat
    ret['route_stat'] = route_stat
    ret['stops_left'] = stops_left

    #return ret
    return render_to_response('stats.html', ret)

