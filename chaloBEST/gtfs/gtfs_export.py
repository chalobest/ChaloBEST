
from mumbai.models import *


routebeer = []


def routeWithLocationData(route):
    # get the route detail
    routeDetails = RouteDetail.objects.filter(route_code=route.code).order_by('serial')

    for rd in routeDetails :        
        if rd.stop.point is None:
            return False
        else:
            pass
    return True

def getRoutesHavingAllLocs():
    filteredroutes = []
    for route in Route.objects.all():
        if routeWithLocationData(route):
            filteredroutes.append(route)

    return filteredroutes


def export_routes():    
    pointstoplist = Stop.objects.filter(point__isnull=False)

    for rd in RouteDetail.objects.all():
        if rd.stop in pointstoplist :
            routebeer.append(rd)

