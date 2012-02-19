from models import *
from ox.django.shortcuts import get_object_or_404_json, render_to_json_response
from django.contrib.auth.decorators import login_required


def route(request, alias):
    route = get_object_or_404_json(Route, alias=alias)
    stops = [r.stop.get_geojson() for r in RouteDetail.objects.filter(route=route)]
    return render_to_json_response({
        'route': route.get_dict(),
        'stops': {
            'type': 'FeatureCollection',
            'features': stops
        }
    })


def stop:(request, id):
    if request.POST:
        if not id:
            stop = Stop() #FIXME: should this return an error instead?
        else:
            stop = get_object_or_404_json(Stop, id=id)
        return stop.from_geojson(request.POST)
    else:
        stop = get_object_or_404_json(Stop, id=id)
        return stop.get_geojson()
