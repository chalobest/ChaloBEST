# Create your views here.
from models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from fuzzywuzzy import process as fuzzprocess

def index(request):
    return render_to_response("index.html", {})

def routes(request):
    context = RequestContext(request, {
        'routes': Route.objects.all()
    })
    return render_to_response("routes.html", context)

def route(request, alias):
    route = get_object_or_404(Route, alias=alias)
    routeDetails = RouteDetail.objects.filter(route=route).order_by('serial')
    context = RequestContext(request, {
        'route': route,
        'routeDetails': routeDetails
    })
    return render_to_response("route.html", context)

def areas(request):
    context = RequestContext(request, {
        'areas': Area.objects.all()
    })
    return render_to_response("areas.html", context)    

def area(request, name):
    area = get_object_or_404(Area, name=name)
    stops = Stop.objects.filter(area=area).order_by('name')
    context = RequestContext(request, {
        'area': area,
        'stops': stops
    })
    return render_to_response("area.html", context)


def stop(request, slug):
    stop = get_object_or_404(Stop, slug=slug)
    context = RequestContext(request, {
        'stop': stop
    })
    return render_to_response("stop.html", context)


def editstops(request):
    context = RequestContext(request, {})
    return render_to_response("editstops.html", context)


def buseditor(request):
    context = RequestContext(request, {})
    return render_to_response("buseditor.html", context)


def stats(request):
    total_stops_left = Stop.objects.filter(point=None).count()
    total_stops = Stop.objects.count()
    areas = []
    for a in Area.objects.all():
        stops = Stop.objects.filter(area=a)
        d = {
            'area': a,
            #'area_name': a.name,
            'total_stops': stops.count(),
            'remaining_stops': stops.filter(point=None).count(),
            'stops_done': stops.filter(point__isnull=False).count(),

        }
        areas.append(d)
    routes = []
    for r in Route.objects.all():
        stops = Stop.objects.filter(routedetail__route=r)
        d = {
            'route': r,
            #'route_name': r.name,
            'total_stops': stops.count(),
            'remaining_stops': stops.filter(point=None).count(),
            'stops_done': stops.filter(point__isnull=False).count(),
        }
        routes.append(d)

    areas_sorted = sorted(areas, key=lambda k: k['remaining_stops']) 
    
    routes_sorted = sorted(routes, key=lambda k: k['remaining_stops']) 

    routes  = routes_sorted
    areas = areas_sorted
    routes.reverse()
    areas.reverse()

    context = {
        'total_stop_count': total_stops,
        'total_stops_left': total_stops_left,
        'areas': areas,
        'routes': routes
    }
    #return context
    return render_to_response("stats.html", context)



@login_required
def fuzzystops(request):
#    import pdb
    froms_arr = []
    tos_arr = []
    for unr in UniqueRoute.objects.all():
        s1 = unr.from_stop.name.lower()
        s2 = unr.from_stop_txt.lower()
        from_ratio = fuzzprocess.ratio(s1,s2)
        if from_ratio < 50:
            froms_arr.append(
                (unr, from_ratio,)
            ) 
        s3 = unr.to_stop.name.lower()
        s4 = unr.to_stop_txt.lower()
        to_ratio = fuzzprocess.ratio(s3,s4)
        if to_ratio < 50:
            tos_arr.append(
                (unr, to_ratio,)
            )
            
    froms_arr.sort(key=lambda item: item[1])
    tos_arr.sort(key=lambda item: item[1])
    context = RequestContext(request, {
        'fuzzy_froms': [item[0] for item in froms_arr],
        'fuzzy_tos': [item[0] for item in tos_arr]
    })
#    pdb.set_trace()
    return render_to_response("fuzzystops.html", context)
