from mumbai.models import *
import json
from settings import *
from os.path import join
import csv
import sys

def routeWithLocationData(route):
    '''
    Tests a  route if it has stop location data for each stop on the route.    
    '''
    # get the route detail
    routeDetails = RouteDetail.objects.filter(route_code=route.code).order_by('serial')

    #unrlist = UniqueRoute.objects.filter('route'=route)
    #for unr in unrlist:
    
    for rd in routeDetails :        
        if rd.stop.point is None:
            return False
        else:
            pass
    return True

def getRoutesHavingAllLocs():
    '''
    Gets routes having stop location data for each stop on the route.
    '''
    filteredroutes = []
    for route in Route.objects.all():
        if routeWithLocationData(route):
            filteredroutes.append(route)

    return filteredroutes



def routeWithSomeLocationData(route,limit):
    '''
    Gets stoplist for a route which has at most <limit> no of stops without location data.
    '''    
    # Get the route details
    routeDetails = RouteDetail.objects.filter(route_code=route.code).order_by('serial')
    # check for routes having less than three errors in stops, and send stops back.
    stoplist =[]
    errs = 0    
    for rd in routeDetails:        
        if rd.stop.point is None:
            # stop does not have point
            errs+=1
            if errs <= limit :
                stoplist.append(rd.stop.code)
        else:
            pass        

    if errs <=limit:
        return dict({'route':route, 'neededstops':len(stoplist) })
    else:
        return None

def getRoutesHavingSomeLocs(limit):
    '''
    Gets those routes which have at most <limit> no of stops without location data.
    '''    
    filteredroutes = []
    no_of_routes = 0
    for route in Route.objects.all():
        data= routeWithSomeLocationData(route, limit)
        if data:
            no_of_routes+=1
            filteredroutes.append(data)

    print "No of routes::",no_of_routes
    return filteredroutes


def export_routes(routebeer):        
    #routebeer = getRoutesHavingAllLocs()     
    f = make_csv_writer("routes.txt")
    f.writerow(["route_id" ,"route_short_name","route_long_name","route_type"])
    for route in routebeer:
        try:
            # data checks here
            f.writerow([route.code,route.alias[0:3],route.from_stop_txt + " - " + route.to_stop_txt,3])
        except:
            pass

def make_csv_writer(filename):
    return csv.writer(open(join(PROJECT_ROOT, "gtfs", filename), "w"), delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

def export_stops(routelist):
    stoplist = []
    for route in routelist:
        rds = RouteDetail.objects.filter(route=route).select_related()
        stoplist.extend(rd.stop for rd in rds)
            
    stoplist = list(set(stoplist))
    f = make_csv_writer("stops.txt")
    f.writerow(["stop_id" ,"stop_name","stop_lat","stop_lon"])
    for stop in stoplist:
        try:
            # data checks here 
            # stop_code is used for stop_id as its BEST specfic..
            # 
            f.writerow([stop.id,stop.name,stop.point.coords[1],stop.point.coords[0]])
        except:
            pass

def export_agency():
    f = make_csv_writer("agency.txt")

    # also
    f.writerow(["agency_id", "agency_name","agency_url","agency_timezone","agency_lang"])
    f.writerow(["BEST","BrihanMumbai Electric Supply & Transport","http://www.bestundertaking.com/","Asia/Kolkata","en"])

    #f.writerow(["agency_id" ,"agency_name","agency_url","agency_timezone"])
    #f.writerow([1 ,"BEST","www.chalobest.in","Asia/Kolkata"])


            # stop_code is used for stop_id as its BEST specfic..

SERVICE_SCHEDULE = [
    {'id':0,'code':'MS','days':[1,2,3,4,5,6]},
    {'id':1,'code':'HOL','days':[7,8]}, # should be only 8
    {'id':2,'code':'SUN','days':[7]},
    {'id':3,'code':'MF&HOL','days':[1,2,3,4,5,8]},
    {'id':4,'code':'SAT','days':[6]},
    {'id':5,'code':'MF','days':[1,2,3,4,5]},
    {'id':6,'code':'SH','days':[7,8]},
    {'id':7,'code':'AD','days':[1,2,3,4,5,6,7,8]},
    {'id':8,'code':'SAT&SUN','days':[6,7]},
    {'id':9,'code':'MS&HOL','days':[1,2,3,4,5,6,8]},
    {'id':10,'code':'FW','days':[1,2,3,4,5,6,7]},
    {'id':11,'code':'SAT/SH','days':[6,7,8]},
    {'id':12,'code':'SAT&HOL','days':[6,8]},
    {'id':13,'code':'SAT&SH','days':[6,7,8]},
    {'id':14,'code':'SAT/SUND&HOL','days':[6,7,8]},
    {'id':15,'code':'S/H','days':[7,8]},
    {'id':16,'code':'SAT,SUN&HOL','days':[6,7,8]}
    ]


def export_calendar():
    f = make_csv_writer("calendar.txt")
    f.writerow(["service_id" ,"monday","tuesday","wednesday","thursday","friday","saturday","sunday","start_date","end_date"])

    start_date="20000101" #YYYYMMDD format
    end_date="20500101" #YYYYMMDD format

    schedule = SERVICE_SCHEDULE

    for ss in schedule:
        try:
            # data checks here 
            running = [1 if day in ss['days'] else 0 for day in range(1,8)]
            # ternary operation :::: ('false','true')[condition]
            f.writerow([ss['code']] + running + [start_date,end_date])
        except:
            print "Error:", str(ss) + '\t' +  str(sys.exc_info()[0]) + '\n'                
def generate_trips(n=None):
    schedules = RouteSchedule.objects.all()
    if n is not None: schedules = schedules[:n]
    for schedule in schedules:
        route = schedule.unique_route.route
        days = schedule.schedule_type
        for direction in ("UP","DOWN"):
            trip_id = "%s_%s_%s" %(route.code, days, direction)
            yield schedule, route, direction, trip_id

def export_trips(routelist):
    f = make_csv_writer("trips.txt")
    for schedule, route, direction, trip_id in generate_trips():
        if route not in routelist: continue
        f.writerow([route.code, schedule.schedule_type, trip_id])
    # we need to get UniqueRoutes for each route, that is one trip, since it is based on service_id which shows days_of_run.
    # we need to be careful here because a filter queryset for UniqueRoutes can differ in order and a naming based on this order 
    # will not be consistent. Its good to use a uniqueroute-serial number.
    #for r in routelist: 
    """
        try:
            # data checks here 

            # ternary operation :::: ('false','true')[condition]
            f.writerow([ss['code'],
                               (0,1)[ss['days'].__contains__(1)],
                               (0,1)[ss['days'].__contains__(2)],
                               (0,1)[ss['days'].__contains__(3)],
                               (0,1)[ss['days'].__contains__(4)],
                               (0,1)[ss['days'].__contains__(5)],
                               (0,1)[ss['days'].__contains__(6)],
                               (0,1)[ss['days'].__contains__(7)],
                               start_date,
                               end_date
                               ])            
        except:
            print "Error:", str(ss) + '\t' +  str(sys.exc_info()[0]) + '\n'                
            """

def getserial(rdlist,stop):
    #check if rdlist is of a ring route..
    if rdlist[0].route.code[3]== 'R' or '4' :
        # write ring specific code here. rings have multiple occuring stops, which one to choose??
        return None    

    for rd in rdlist:
        if(rd.stop==stop):
            return rdlist.index(rd)
               
def runtime_in_minutes(schedule):
    runtime = schedule.runtime1 or schedule.runtime2 or schedule.runtime3 or schedule.runtime4
    if runtime: return runtime
    t_from, t_to = schedule.first_from, schedule.first_to
    if not t_from or not t_to:
        t_from, t_to = schedule.last_from, schedule.last_to
    return abs(t_from.hour * 60 + t_from.minute -
              (t_to.hour * 60 + t_to.minute))
        
def export_stop_times(routelist):
    f = make_csv_writer("stop_times.txt")
    f.writerow(["trip_id","arrival_time","departure_time","stop_id","stop_sequence"])
    for schedule, route, direction, trip_id in generate_trips():
        if route not in routelist: continue
        order = "" if direction == "UP" else "-"
        details = list(RouteDetail.objects.filter(route=route).order_by(order+"serial"))
        initial_time = departure_time = schedule.first_to if direction == "UP" else schedule.first_from
        arrival_time = ""
        for sequence, detail in enumerate(details):
            if sequence == len(details) - 1:
                arrival = initial_time.hour * 60 + initial_time.minute + runtime_in_minutes(schedule)
                arrival_time = "%02d:%02d:00" % (int(arrival/60), arrival % 60)
            f.writerow([trip_id,arrival_time,departure_time,detail.stop.code,sequence])
            departure_time = ""

    #routelist = getRoutesHavingAllLocs()    

    #1. get routeDetails
    #2. get unique routes as unr and the routeDetails subset as rd_subset for that uniqueroute
    #3. get unr.routeschedule as unr.rs ?? why is it multiple?
    #4. get total distance as tdist from rd_subset
    #5. get runtime from unr.rs 
    #6. if runtime1 is null, then runtime = abs(first_from - first_to)    
    #7. avgspeed = tdist/runtime... if runtime is not available then ??
    #8.  

    """
    for r in routelist:
        rdlist = RouteDetail.objects.filter(route=r).order_by('serial')    
        sr_no=0
        unrs  =  UniqueRoute.objects.filter(route=r).order_by('id')
        
        for unr in unrs:
            from_stop = unr.from_stop
            to_stop = unr.to_stop
            rd_subset = rdlist[getserial(rdlist,from_stop):getserial(rdlist,to_stop)]
            dist=0
            for rd in rd_subset:
                dist += rd.km
            runtime = unr.runtime1
            if not runtime:
                rs = unr.routeschedule_set.all()[0]
                #if rs.
            sr_no +=1
            for rd in rd_subset:
                f.writerow([r.code+"_"+sr_no,"","",rd.stop.id,rd.serial])
    """



"""
stop_times.txt
================================================================================================================================================
1. For each route.
2. Get rdlist = routedetails for that route.order_by('serial'). Get UniqueRoutes for the route.
3. --- scenario -- Not considering uniqueroutes--
3.1 For rd in rdlist
73.1.1 filewrite (trip_id,,,stopid,stop.serial)

----alternate scenario
3. For each UniqueRoute, get from_to stops list (rdsubset) from RouteDetail list
for unr in unrs:
from_stop, to_stop
rd_subset  = rdlist[getserial(rdlist,from_stop):getserial(rdlist,to_stop)]
"""


def export_frequencies(routelist):
    f = make_csv_writer("frequencies.txt")
    """
    EACH ROW IN FREQUENCIES
    - For an entry in atlas, [ i.e. a given trip+service_id [subset + schedule days] ] 
    If there are headway timings for diff time slots, eg. 
    h7-11, h11-16, h16-22,h22-25
    
    then
    """
    TIMESPANS = ((None,"07:00:00"),
                 ("07:00:00","11:00:00"),
                 ("11:00:00","17:00:00"),
                 ("17:00:00","20:00:00"),
                 ("20:00:00",None))
    
    f.writerow(["trip_id", "start_time","end_time","headway_secs"])
    for schedule, route, direction, trip_id in generate_trips():
        if route not in routelist: continue
        headway = (schedule.headway1,
                   schedule.headway2,
                   schedule.headway3,
                   schedule.headway4,
                   schedule.headway5)
        for span, (start_time, end_time) in enumerate(TIMESPANS):
            if direction == "UP":
                if start_time is None: start_time = schedule.first_from
                if end_time is None: end_time = schedule.last_from
            else:
                if start_time is None: start_time = schedule.first_to
                if end_time is None: end_time = schedule.last_to
            if headway[span] is not None:
                f.writerow([trip_id, start_time, end_time, headway[span]*60])

def fire_up():
    routelist = getRoutesHavingAllLocs()
    export_routes(routelist)
    #export_stops()
    export_frequencies()
    export_stop_times()
    export_calendar()
    export_trips()
    export_agency()
    

