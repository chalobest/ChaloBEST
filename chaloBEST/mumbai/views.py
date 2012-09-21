# Create your views here.
from models import *
from django.shortcuts import render_to_response, get_object_or_404
from ox.django.shortcuts import get_object_or_404_json, render_to_json_response

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from fuzzywuzzy import process as fuzzprocess
from django.http import HttpResponse

def index(request):
    areas = Area.objects.all().order_by('name')
    
    context = RequestContext(request, {
        'areas': areas
    })
    return render_to_response("innov/index.html", context)


def about(request):
    context = RequestContext(request, {})
    return render_to_response("innov/about_chalobest.html", context)

def android(request):
    context = RequestContext(request, {})
    return render_to_response("innov/android.html", context)

def join_us(request):
    context = RequestContext(request, {})
    return render_to_response("innov/joinus.html", context)

def sms(request):
    context = RequestContext(request, {})
    return render_to_response("innov/SMS.html", context)

def contact(request):
    context = RequestContext(request, {})
    return render_to_response("innov/contactus.html", context)

def login(request):
    return render_to_response('login.html',c, context_instance=RequestContext(request))

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

@login_required
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
    start = int(request.GET.get("start", 0))
    end = int(request.GET.get("end", start + 50))
    show_checked = request.GET.get("show_checked", False)
    unrs = []
    for unr in UniqueRoute.objects.all().order_by('route__code'):
        
        if FuzzyStopMatch.objects.filter(unr=unr).filter(checked=True).count() > 0:
            if not show_checked:
                continue
        else:
            if show_checked:
                continue        

        rds = RouteDetail.objects.filter(route=unr.route).order_by('serial')
        unrd = {}
        fs = False
        ls = False
        if unr.from_stop==rds[0].stop:
            fs=True
        else:
            fs=False

        if unr.to_stop==rds[len(rds)-1].stop:
            ls=True
        else:
            ls=False

        unrs.append({'unr':unr,'stop_is_first':fs,'stop_is_last':ls})
#    import pdb
#    pdb.set_trace()
    if end > len(unrs):
        end = len(unrs)
 
    context = RequestContext(request, {
        'unrs': unrs[start:end],
        'total': len(unrs),
        'start': start,
        'end': end
    })
    return render_to_response("fuzzystops.html", context)


@login_required
@csrf_exempt
def fuzzystops_edit(request):
    unr_id = request.POST.get("id", 0)
    unr = UniqueRoute.objects.get(pk=unr_id)
    from_stop_id = int(request.POST.get("from_stop"))
    to_stop_id = int(request.POST.get("to_stop"))    
    unr.from_stop_id = from_stop_id
    unr.to_stop_id = to_stop_id
    unr.save()
    change_all = request.POST.get("change_all", False)
    if change_all:
        from_stop_txt = unr.from_stop_txt
        to_stop_txt = unr.to_stop_txt
        for u in UniqueRoute.objects.filter(from_stop_txt=from_stop_txt):
            u.from_stop = from_stop_id
            u.save()
        for u in UniqueRoute.objects.filter(to_stop_txt=from_stop_txt):
            u.to_stop = from_stop_id
            u.save()
        for u in UniqueRoute.objects.filter(to_stop_txt=to_stop_txt):
            u.to_stop = to_stop_id
            u.save()
        for u in UniqueRoute.objects.filter(from_stop_txt=to_stop_txt):
            u.from_stop = to_stop_id
            u.save()
    mark_checked = request.POST.get("mark_checked", False)
    if mark_checked:
        fsm, created = FuzzyStopMatch.objects.get_or_create(unr=unr)
        fsm.checked = True
        fsm.save()
    return HttpResponse("ok")


        

#@login_required
#def fuzzystops(request):
##    import pdb
#    froms_arr = []
#    tos_arr = []
#    for unr in UniqueRoute.objects.all():
#        s1 = unr.from_stop.name.lower()
#        s2 = unr.from_stop_txt.lower()
#        from_ratio = fuzzprocess.ratio(s1,s2)
#        if from_ratio < 70:
#            froms_arr.append(
#                (unr, from_ratio,)
#            ) 
#        s3 = unr.to_stop.name.lower()
#        s4 = unr.to_stop_txt.lower()
#        to_ratio = fuzzprocess.ratio(s3,s4)
#        if to_ratio < 70:
#            tos_arr.append(
#                (unr, to_ratio,)
#            )
#            
#    froms_arr.sort(key=lambda item: item[1])
#    tos_arr.sort(key=lambda item: item[1])
#    context = RequestContext(request, {
#        'fuzzy_froms': [item[0] for item in froms_arr],
#        'fuzzy_tos': [item[0] for item in tos_arr]
#    })
##    pdb.set_trace()
#    return render_to_response("fuzzystops.html", context)


def route_headway(request, code):
    """
    Given a route code, gets the current frequency of the buses at the current time.
    """
    route = get_object_or_404(Route, code=code)
    import datetime 
    current_time = datetime.datetime.now()
    day = current_time.isoweekday()
    
    scheds = []
    for rs in RouteSchedule.objects.filter(unique_route__route=route):
        if day in SCHED[rs.schedule_type]:
            scheds.append(rs)    

    
    TIMESPANS = ((None,"06:59:59"),
                 ("07:00:00","10:59:59"),
                 ("11:00:00","16:59:59"),
                 ("17:00:00","19:59:59"),
                 ("20:00:00",None))

    #for s in scheds:
    #    if current_time< time_of("") 

    return render_to_json_response(        
      {
        'route': route.get_dict(),
        'scheds': [ (s.headway1, s.headway2, s.headway3, s.headway4, str(s.unique_route) ) for s in scheds]
        })


