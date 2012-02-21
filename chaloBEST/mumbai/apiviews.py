from models import *
from ox.django.shortcuts import get_object_or_404_json, render_to_json_response
from django.contrib.auth.decorators import login_required


def route(request, slug):
    route = get_object_or_404_json(Route, slug=slug)
    stops = [r.stop.get_geojson() for r in RouteDetail.objects.filter(route=route)]
    return render_to_json_response({
        'route': route.get_dict(),
        'stops': {
            'type': 'FeatureCollection',
            'features': stops
        }
    })

def area(request, slug):
    area = get_object_or_404_json(Area, slug=slug)
    stops = [stop.get_geojson() for stop in Stop.objects.filter(area=area)]
    return render_to_json_response({
        'area': area.get_dict(),
        'stops': { 
            'type': 'FeatureCollection',
            'features': stops
        }
    })

def routes(request):
    qset = Route.objects.all()
    if request.GET.has_key('q'):
        q = request.GET.get('q', '')
        qset = qset.filter(alias__icontains=q) #FIXME: make a better Q object
    routes = [route.alias for route in qset]
    return render_to_json_response(routes)


def areas(request):
    qset = Area.objects.all()
    if request.GET.has_key('q'):
        q = request.GET.get('q', '')
        qset = qset.filter(display_name__icontains=q)    
    areas = [area.slug for area in qset]
    return render_to_json_response(areas)

def stops(request):
    qset = Stop.objects.all()
    if request.GET.has_key('q'):
        q = request.GET.get('q', '')
        qset = qset.filter(display_name__icontains=q) #FIXME: This definitely needs to be a Q object with OR lookups for area name, road name, etc.    
    return render_to_json_response({
        'type': 'FeatureCollection',
        'features': [stop.get_geojson() for stop in qset]
    })
   


def stop(request, slug):
    if request.POST:
        if not slug:
            stop = Stop() #FIXME: should this return an error instead?
        else:
            stop = get_object_or_404_json(Stop, slug=slug)
        return render_to_json_response(stop.from_geojson(request.POST))
    else:
        stop = get_object_or_404_json(Stop, slug=slug)
        return render_to_json_response(stop.get_geojson()) #FIXME: please don't repeat this code, its retarded.
