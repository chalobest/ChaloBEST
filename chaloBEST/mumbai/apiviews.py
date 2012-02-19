from models import *
from ox.django.shortcuts import get_object_or_404_json, render_to_json_response

def route(request, code):
    route = get_object_or_404_json(Route, code=code)
    stops = [r.stop.get_geojson() for r in RouteDetail.objects.filter(route=route)]
    return render_to_json_response({
        'route': route.get_dict(),
        'stops': {
            'type': 'FeatureCollection',
            'features': stops
        }
    })
