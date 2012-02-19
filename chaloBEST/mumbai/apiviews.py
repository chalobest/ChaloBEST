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
