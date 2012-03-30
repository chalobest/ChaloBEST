from mumbai.models import *

# for Road, Area, Landmark, Stop
def copynames2display_name():
    print "Copying names to display_name field..."
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

                

