from models import *
from ox.django.shortcuts import get_object_or_404_json, render_to_json_response
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt

def route(request, slug):
    srid = int(request.GET.get("srid", 4326))
    route = get_object_or_404_json(Route, slug=slug)
    stops = [r.stop.get_geojson(srid=srid) for r in RouteDetail.objects.filter(route=route)]
    return render_to_json_response({
        'route': route.get_dict(),
        'stops': {
            'type': 'FeatureCollection',
            'features': stops
        }
    })

def area(request, slug):
    srid = int(request.GET.get("srid", 4326))
    area = get_object_or_404_json(Area, slug=slug)
    stops = [stop.get_geojson(srid=srid) for stop in Stop.objects.filter(area=area)]
    return render_to_json_response({
        'area': area.get_dict(),
        'stops': { 
            'type': 'FeatureCollection',
            'features': stops
        }
    })

def routes(request):
    q = request.GET.get("q", "")
    if q != '':
        qset = Route.objects.filter(alias__icontains=q)
    else:
        qset = Route.objects.all()
    routes = [route.alias for route in qset]
    return render_to_json_response(routes)


def areas(request):
    q = request.GET.get("q", "")
    if q != '':
        qset = Area.objects.find_approximate(q, 0.33)
    else:
        qset = Area.objects.all()
    areas = [area.slug for area in qset]
    return render_to_json_response(areas)

def stops(request):
    q = request.GET.get("q", "")
    if q != '':
        qset = Stop.objects.find_approximate(q, 0.33)
    else:
        qset = Stop.objects.all()
    srid = int(request.GET.get("srid", 4326))   
    return render_to_json_response({
        'type': 'FeatureCollection',
        'features': [stop.get_geojson(srid=srid) for stop in qset]
    })
   

@csrf_exempt
def stop(request, slug):
    srid = int(request.GET.get("srid", 4326))
    if request.POST and request.POST.has_key('geojson'):
        if not slug:
            stop = Stop() #FIXME: should this return an error instead?
        else:
            stop = get_object_or_404_json(Stop, slug=slug)
        geojson = json.loads(request.POST['geojson'])
        return render_to_json_response(stop.from_geojson(geojson, srid))
    else:
        stop = get_object_or_404_json(Stop, slug=slug)        
        return render_to_json_response(stop.get_geojson(srid=srid)) #FIXME: please don't repeat this code, its retarded.
