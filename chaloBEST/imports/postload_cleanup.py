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

def make_stage_info():
    for rd in RouteDetail.objects.all():
        if rd.km:
            rd.stage=True
            rd.save()
                

def make_type_info():
    for r in Route.objects.all():
        r.route_type = RouteType.objects.get(code=str(r.code)[3])
        r.save()

def make_code_info():
    for r in Route.objects.all():
        if r.code.isdigit():
            r.code3 = str(r.code)[0:3]
            r.save()

def do():
    copynames2display_name()
    make_code_info()
    make_type_info()
    make_stage_info()

