from mumbai.models import *


"Road, Area, Landmark, Stop"

def copynames2display_name():
    for obj in Stop.objects.all():
        obj.display_name =obj.name
        obj.save()
    for obj in Area.objects.all():
        obj.display_name =obj.name
        obj.save()
    for obj in Landmark.objects.all():
        obj.display_name =obj.name
        obj.save()
    for obj in Road.objects.all():
        obj.display_name =obj.name
        obj.save()

def copydefaultStopLocations():
    for stop in Stop.objects.all():
        stop.stop = stop.stoplocation_set.all()[0]
    

