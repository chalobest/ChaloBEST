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
    filedude = csv.writer(open(join(PROJECT_ROOT, "gtfs/routes.txt"), "w"), delimiter=",")
    filedude.writerow(["route_id" ,"route_short_name","route_long_name","route_type"])
    for route in routebeer:
        try:
            # data checks here
            filedude.writerow([route.code,route.alias[0:3],route.from_stop_txt + " - " + route.to_stop_txt,3])
        except:
            pass

def export_stops(olist):
    filedude = csv.writer(open(join(PROJECT_ROOT, "gtfs/stops.txt"), "w"), delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    filedude.writerow(["stop_id" ,"stop_name","stop_lat","stop_lon"])
    for stop in olist:
        try:
            # data checks here 
            # stop_code is used for stop_id as its BEST specfic..
            # 
            filedude.writerow([stop.id,stop.name,stop.point.coords[1],stop.point.coords[0]])
        except:
            pass

def export_agency():
    filedude = csv.writer(open(join(PROJECT_ROOT, "gtfs/agency.txt"), "w"), delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # also
    filedude.writerow(["agency_id", "agency_name","agency_url","agency_timezone","agency_lang"])
    filedude.writerow(["BEST","BrihanMumbai Electric Supply & Transport","http://www.bestundertaking.com/","Asia/Kolkata","en"])

    #filedude.writerow(["agency_id" ,"agency_name","agency_url","agency_timezone"])
    #filedude.writerow([1 ,"BEST","www.chalobest.in","Asia/Kolkata"])


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
    filedude = csv.writer(open(join(PROJECT_ROOT, "gtfs/calendar.txt"), "w"), delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    filedude.writerow(["service_id" ,"monday","tuesday","wednesday","thursday","friday","saturday","sunday","start_date","end_date"])

    start_date="20000101" #YYYYMMDD format
    end_date="20500101" #YYYYMMDD format

    schedule = SERVICE_SCHEDULE

    for ss in schedule:
        try:
            # data checks here 

            # ternary operation :::: ('false','true')[condition]
            filedude.writerow([ss['code'],
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



def export_trips():
    filedude = csv.writer(open(join(PROJECT_ROOT, "gtfs/trips.txt"), "w"), delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    filedude.writerow(["route_id","service_id","trip_id"])
    filedude.writerow(["2820","MS","2820_1"])
    #filedude.writerow(["246","HOL","282_2"])
    #filedude.writerow(["246","SUN","282_3)"])

    filedude.writerow(["2894","MS","2894_1"])
    #filedude.writerow(["253","HOL","289_2"])
    #filedude.writerow(["253","SUN","289_3"])

    # we need to get UniqueRoutes for each route, that is one trip, since it is based on service_id which shows days_of_run.
    # we need to be careful here because a filter queryset for UniqueRoutes can differ in order and a naming based on this order 
    # will not be consistent. Its good to use a uniqueroute-serial number.
    #for r in routelist: 
    """
        try:
            # data checks here 

            # ternary operation :::: ('false','true')[condition]
            filedude.writerow([ss['code'],
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
               
        
def export_stop_times(routelist):
    filedude = csv.writer(open(join(PROJECT_ROOT, "gtfs/stop_times.txt"), "w"), delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    filedude.writerow(["trip_id","arrival_time","departure_time","stop_id","stop_sequence"])
    #routelist = getRoutesHavingAllLocs()    

    #1. get routeDetails
    #2. 
    for r in routelist:
        rds = RouteDetail.objects.filter(route=r).order_by('serial')    
        sr_no=0
        for unr in UniqueRoute.objects.filter(route=r).order_by('id'):
            from_stop = unr.from_stop
            to_stop = unr.to_stop        
            rd_subset  = rds[getserial(rdlist,from_stop):getserial(rdlist,to_stop)]
            sr_no +=1 
            for rd in rd_subset:
                filedude.writerow([r.code+"_"+sr_no,"","",rd.stop.id,rd.serial])



"""
stop_times.txt
================================================================================================================================================
1. For each route.
2. Get rdlist = routedetails for that route.order_by('serial'). Get UniqueRoutes for the route.
3. --- scenario -- Not considering uniqueroutes--
3.1 For rd in rdlist
3.1.1 filewrite (trip_id,,,stopid,stop.serial)

----alternate scenario
3. For each UniqueRoute, get from_to stops list (rdsubset) from RouteDetail list
for unr in unrs:
from_stop, to_stop
rd_subset  = rdlist[getserial(rdlist,from_stop):getserial(rdlist,to_stop)]
"""


def export_frequencies():
    filedude = csv.writer(open(join(PROJECT_ROOT, "gtfs/frequencies.txt"), "w"), delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    """
    EACH ROW IN FREQUENCIES
    - For an entry in atlas, [ i.e. a given trip+service_id [subset + schedule days] ] 
    If there are headway timings for diff time slots, eg. 
    h7-11, h11-16, h16-22,h22-25
    
    then
    """
    
    filedude.writerow(["trip_id", "start_time","end_time","headway_secs"])
    filedude.writerow(["282_1","07:00:00","11:00:00",360])
    filedude.writerow(["282_1","11:00:00","16:00:00",420])
    filedude.writerow(["282_1","16:00:00","22:00:00",480])
    filedude.writerow(["282_1","07:00:00","11:00:00",360])
    filedude.writerow(["289_1","07:00:00","11:00:00",600])
    filedude.writerow(["289_1","11:00:00","16:00:00",420])
    filedude.writerow(["289_1","16:00:00","22:00:00",420])
    filedude.writerow(["289_1","07:00:00","11:00:00",540])
    

    
