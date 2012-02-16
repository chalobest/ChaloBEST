
from mumbai.models import *
import json
from settings import *
from os.path import join
import csv
import sys

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


def export_routes(routebeer):        
    #routebeer = getRoutesHavingAllLocs()     
    filedude = csv.writer(open(join(PROJECT_ROOT, "gtfs/routes.txt"), "w"), delimiter=",")
    filedude.writerow(["route_id" ,"route_short_name","route_long_name","route_type"])
    for route in routebeer:
        try:
            # data checks here
            filedude.writerow([route.id,route.alias,route.from_stop_txt + " - " + route.to_stop_txt,3])
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
            filedude.writerow([stop.code,stop.name,stop.point.coords[1],stop.point.coords[0]])
        except:
            pass

def export_agency():
    filedude = csv.writer(open(join(PROJECT_ROOT, "gtfs/agency.txt"), "w"), delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # also
    #filedude.writerow(["agency_id", "agency_name","agency_url","agency_timezone","agency_lang"])
    #filedude.writerow(["BEST","BrihanMumbai Electric Supply & Transport","http://www.bestundertaking.com/","Asia/Kolkata","en"])

    filedude.writerow(["agency_id" ,"agency_name","agency_url","agency_timezone"])
    filedude.writerow([1 ,"BEST","www.chalobest.in","Asia/Kolkata"])


            # stop_code is used for stop_id as its BEST specfic..

SERVICE_SCHEDULE = [
    {'id':0,'code':'MS','days':[1,2,3,4,5,6]},
    {'id':1,'code':'HOL','days':[8]},
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
    filedude.writerow(["246","MS","282(1)"])
    filedude.writerow(["246","HOL","282(2)"])
    filedude.writerow(["246","SUN","282(3)"])

    filedude.writerow(["253","MS","289(1)"])
    filedude.writerow(["253","HOL","289(2)"])
    filedude.writerow(["253","SUN","289(3)"])

    # we need to get UniqueRoutes for each route, that is one trip, since it is based on service_id which shows days_of_run.
    # we need to be careful here because a filter queryset for UniqueRoutes can differ in order and a naming based on this order 
    # will not be consistent. Its good to use a uniqueroute-serial number.

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

               
        
    

