from mumbai.models import *
import json
from settings import *
from os.path import join
import csv
import sys
import datetime
from itertools import dropwhile
import copy    
from fuzzywuzzy import process as fuzzprocess
import pdb

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
    for route in Route.objects.all().select_related():
        isOK=False
        if routeWithLocationData(route): 
            isOK=True 
        else:
            isOK=False

        if isOK:
            filteredroutes.append(route)

    return filteredroutes



def getCompleteRoutes_old(routelist):
    #get routes having all stop locaions
    filteredroutes = []
    isComplete = True
        
    for route in routelist:
        # check if all stops have locs
        isComplete = True
        if routeWithLocationData(route):
            # check if Unique Routes have distance
            unrs = route.uniqueroute_set.all()
            for unr in unrs:
                if unr.distance:
                    rsset= unr.routeschedule_set.all()
                    for rs in rsset:
                        if rs.runtime1 and rs.runtime2 and rs.runtime3 and rs.runtime4 and rs.headway1 and rs. headway2 and rs.headway3 and rs.headway4 and rs.headway5 and rs.first_from and rs.first_to and rs.last_from and rs.last_to:
                            filteredroutes.append(route)
                        else:
                            isComplete = False
                            continue
                else:
                    isComplete = False
                    continue
        

    return list(set(filteredroutes))

from operator import itemgetter


def getCompleteRoutes2():
    #get routes having all stop locaions

    isComplete = True
    
    routelist =[]
    rtdt = {}

    for rs in RouteSchedule.objects.select_related():
        flag = 0
        rtdt[rs.unique_route.route] = True

        if rs.runtime1 and rs.runtime2 and rs.runtime3 and rs.runtime4 and rs.headway1 and rs. headway2 and rs.headway3 and rs.headway4 and rs.headway5 and rs.first_from and rs.first_to and rs.last_from and rs.last_to:   
            pass
        else:
            rtdt[rs.unique_route.route] = False

        if rs.unique_route.distance:
            pass
        else:
            rtdt[rs.unique_route.route] = False

            
    for k,v in rtdt.iteritems():
        if v:
            routelist.append(k)
        
    return routelist
        

def getCompleteRoutes():
    rset = set()

    for rs in RouteSchedule.objects.select_related():
        if not( rs.runtime1 and rs.runtime2 and rs.runtime3 and rs.runtime4 and rs.headway1 and rs. headway2 and rs.headway3 and rs.headway4 and rs.headway5):
# and rs.first_from and rs.first_to and rs.last_from and rs.last_to):           
            try:
                rset.remove(rs.unique_route.route)
            except KeyError:
                pass
        else:
            # other criteria
            if routeWithLocationData(rs.unique_route.route) and rs.unique_route.distance:
                rset.add(rs.unique_route.route)
    return list(rset)



"""
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
"""

def rindex(lst, item):
    """
    gets last occurence of item from list
    """
    try:
        return dropwhile(lambda x: lst[x] != item, reversed(xrange(len(lst)))).next()
    except StopIteration:
        raise ValueError, "rindex(lst, item): item not in list"


def make_csv_writer(filename):
    return csv.writer(open(join(PROJECT_ROOT, "gtfs", "gtfs_mumbai_bus", filename), "w"), delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

   
def export_routes(routebeer):        
    #routebeer = getRoutesHavingAlLocs()     
    f = make_csv_writer("routes.txt")
    f.writerow(["route_id","agency_id","route_short_name","route_long_name","route_type"])

    for route in routebeer:
        try:
            # data checks here
            f.writerow([route.code,"BEST",route.alias[0:3],route.from_stop_txt + " - " + route.to_stop_txt,3])
        except:
            pass

def export_agency():
    f = make_csv_writer("agency.txt")

    # also
    f.writerow(["agency_id", "agency_name","agency_url","agency_timezone","agency_lang"])
    f.writerow(["BEST","BEST","http://www.bestundertaking.com/","Asia/Kolkata","en"])

    #f.writerow(["agency_id" ,"agency_name","agency_url","agency_timezone"])
    #f.writerow([1 ,"BEST","www.chalobest.in","Asia/Kolkata"])



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
    {'id':16,'code':'SAT,SUN&HOL','days':[6,7,8]},
    {'id':17,'code':'FH','days':[5,8]},   
    {'id':18,'code':'MS&SUN','days':[1,2,3,4,5,7]},
    ]

#{'id':18,'code':'2nd &4th','days':[7,8]},
# FH indicates what? full week + holidays??
# HOL holidays means only the exceptions as defined in calendar_dates.txt. this needs to be converted separately. 
# done here only to get the other components of gtfs up.

feed_start_date="2012-07-01" # YYYY-MM-DD
feed_end_date="2012-11-30" # YYYY-MM-DD
start_date_str = ''
end_date_str = ''

def export_calendar():
    f = make_csv_writer("calendar.txt")
    f.writerow(["service_id" ,"monday","tuesday","wednesday","thursday","friday","saturday","sunday","start_date","end_date"])

    f2 = make_csv_writer("calendar_dates.txt")
    f2.writerow(["service_id","date","exception_type"])

    # start date
    d = feed_start_date.split("-")    
    s_year=d[0]
    s_month=d[1]
    s_day=d[2]

    
    # end date
    d = feed_end_date.split("-")    
    e_year=d[0]
    e_month=d[1]
    e_day=d[2]

    start_date_str = s_year+s_month+s_day # "20120301" #YYYYMMDD format
    end_date_str = e_year+e_month+e_day # "20120630" #YYYYMMDD format 

    start_date = datetime.date(int(s_year),int(s_month),int(s_day))
    end_date = datetime.date(int(e_year),int(e_month),int(e_day)) 

    schedule = SERVICE_SCHEDULE

    for ss in schedule:
        try:
            # data checks here 
            running = [1 if day in ss['days'] else 0 for day in range(1,8)]
            if 8 in ss['days']:
                # check holidays, if in time period between start_date and stop_date then, load in cal_dates
                for hol in Holiday.objects.all():
                    if hol.date > start_date and hol.date < end_date:
                        f2.writerow([ss['code']]+ [hol.date.__str__().replace("-","")] + ["1"])
            
            f.writerow([ss['code']] + running + [start_date_str,end_date_str])
        except:
            print "Error:", str(ss) + '\t' +  str(sys.exc_info()[0]) + '\n'                

def export_feed_info():
    f = make_csv_writer("feed_info.txt")
    f.writerow(["feed_publisher_name","feed_publisher_url","feed_lang","feed_start_date","feed_end_date","feed_version"])
    f.writerow(["ChaloBEST","http://chalobest.in","en",start_date_str,end_date_str,"0.31"])


def uniquify_list_of_lists(sequence):
    seen = set()
    return [ x for x in sequence if str( x ) not in seen and not seen.add( str( x ) )]

def generate_trips(n=None):
    schedules = RouteSchedule.objects.all()
    if n is not None: schedules = schedules[:n]
    #triplist = []
    for schedule in schedules:
        route = schedule.unique_route.route
        unr = schedule.unique_route
        days = schedule.schedule_type

        for direction in ("UP","DOWN"):
            trip_id = "%s_%s_%s_%s" %(route.code,schedule.id,days, direction)
            #triplist.append([schedule, route, direction, trip_id])
            yield schedule, route, direction, trip_id
    #return uniquify_list_of_lists(triplist)


def generate_trips_unr(n=None):
    schedules = RouteSchedule.objects.all()
    if n is not None: schedules = schedules[:n]
    for schedule in schedules:
        route = schedule.unique_route.route
        unr = schedule.unique_route
        days = schedule.schedule_type

        for direction in ("UP","DOWN"):
            trip_id = "%s_%s_%s_%s" %(route.code,schedule.id,days, direction)
            yield schedule, unr, route, direction, trip_id


def getOverlappingSchedules():
    ret = []
    for unr in UniqueRoute.objects.all().select_related():
        sched_types = unr.routeschedule_set.values('schedule_type').distinct()
        for s in sched_types:
            qset = unr.routeschedule_set.filter(schedule_type=s['schedule_type'])
            if qset.count() > 1:                
                rows = [schedule.__dict__ for schedule in qset]
                ret.append(rows)
    return ret
            

def getRoutesWOverlappingSchedules():
    count = 0
    rslist=[]
    cnt=0
    #return  a list of unrs and rs's which have colliding schedule_type

    for unr in UniqueRoute.objects.all():
        ulist = unr.routeschedule_set.all() 
        stlist=[]        
        rslst = []

        for rs in ulist:
            if rs.schedule_type:
                rslst.append((rs, rs.schedule_type))
                stlist.append(rs.schedule_type)
            else:
                cnt+=1
            

        rsset=[]

        for rs in ulist:
            if rs.schedule_type and (rs, rs.schedule_type) not in rsset:
                rsset.append((rs, rs.schedule_type))             

        if len(rslst) > len(rsset):            
            count+=1
            #reduced_rslst = list(rsset)
            #rslist.append([(rs,st) for (rs, st) in rslst if (rs,st) in reduced_rslst])

    return {'rslist':count, 'rsset':rsset, 'rslst':rslst}
            
            

overlapp_sched = []

def export_trips(routelist):
    f = make_csv_writer("trips.txt")
    f.writerow(["route_id","service_id","trip_id"])
    lst = []
    for schedule, route, direction, trip_id in generate_trips():
        if route not in routelist: continue
        if (route.code, schedule.schedule_type, trip_id) in lst: 
            overlapp_sched.append((route.code, schedule.schedule_type, trip_id))
            continue

        lst.append((route.code, schedule.schedule_type, trip_id))
        f.writerow([route.code, schedule.schedule_type, trip_id])

    # we need to get UniqueRoutes for each route, that is one trip, since it is based on service_id which shows days_of_run.

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

def getserial(rdlist,stop,getFirstStop=True):
    #check if rdlist is of a ring route..
    if rdlist[0].route.code[3] in ['R','4']:
        # write ring specific code here. rings have multiple occuring stops, which one to choose??
        pass
        #return None    
    for rd in rdlist:
        if(rd.stop==stop):
            return rdlist.index(rd)

def checkUniqueRouteStops():
    no_from=set()
    no_to=set()

    for unr in UniqueRoute.objects.all():
        if unr.from_stop not in [s.stop for s in unr.route.routedetail_set.all()]:
            no_from.add(unr)
        if unr.to_stop not in [s.stop for s in unr.route.routedetail_set.all()]:
            no_to.add(unr)
    return {'to_stop_missing':no_from , 'from_stop_missing': no_to}


reversed_rds=[]
mismatched_unrs={"from":[], "to":[]}
multiple_to_stops=[]
badroutes=set()

def get_routedetail_subset(unr, direction):
    """
    Given a uniqueroute, gets the list of stops in it.    
    Algo. 
    1. get routedetail(rd) list
    2. check if rds are reversed
    3. select stops if they are in UP or DOWN route, if a stop is to be removed, transfer the km info to the next or previous stop
    4. get indexes of the stops in the list.
    5. splice the list acc to positions
    6. check if full route, if yes, then ignore calculations, send entire list (only filter up/down stops)
    
    """

    from_stop = unr.from_stop
    to_stop = unr.to_stop    
    code=str(unr.route.code)[3]
    rdlist = list(RouteDetail.objects.filter(route=unr.route).order_by("serial"))
    
    route_reversed = False
    # Sometimes to_stop comes before from_stop in RouteDetail.
    # So reverse the list if that happens.. so a from_stop will always come before a to_stop              
    # reverse list
    for detail in rdlist:
        if detail.stop.id == from_stop.id: break
        if detail.stop.id == to_stop.id:
            rdlist.reverse()
            reversed_rds.append({"unr":unr, "dir":direction})
            route_reversed = True
            break

    # select stops in route for "UP/DOWN" routes respectively
    if direction in ["UP", "up", "U"]:
        lst = [] 
        for pos, rd in enumerate(rdlist):
            if rd.stop.dbdirection == '' or rd.stop.dbdirection == 'U' or rd.stop==unr.from_stop or rd.stop==unr.to_stop:
                lst.append(rd)
            # else:
            #     # add km info of the stop to be removed to next or prev stop, 
            #     if rd.km and pos != len(rdlist)-1:
            #         if rdlist[pos+1].km: # if it next stop has km, 
            #             rdlist[pos+1].km+=rd.km
            #         else:
            #             rdlist[pos+1].km=rd.km
            #     else:
            #         if pos != 0 and not rdlist[pos - 1].km and rd[pos].km:
            #             rdlist[pos+1].km = rd.km
                    
                
    else:
        # for "DOWN" routes
        lst = []
        for pos, rd in enumerate(rdlist):
            if rd.stop.dbdirection == '' or rd.stop.dbdirection ==  'D' or rd.stop==unr.from_stop or rd.stop==unr.to_stop:
                lst.append(rd)
            #else:
                # add km info of the stop to be removed to next or prev stop, 
                # if pos != len(rdlist)-1 and rdlist[pos + 1].km:
                #     rdlist[pos+1].km = rd.km
                # else:
                #     if pos != 0 and rdlist[pos - 1].km:
                #         rdlist[pos+1].km = rd.km
                    
            
    rdlist = lst            
    #pdb.set_trace()


#30 lines below only to get the index positions of the from and to stops in the list. 
    from_index = -1
    to_index= -1

    from_stop_found = 0
    to_stop_found = 0

    # from stop index
    for rd in rdlist:
        if(rd.stop.id==from_stop.id):
            from_index = rdlist.index(rd)
            from_stop_found=1
            break

    if from_stop_found == 0:
        print "From-Stop not found in Route Details for unr.id", unr.id, "unr.from_stop_txt=", unr.from_stop_txt 
        mismatched_unrs['from'].append({"unr":unr,"unr_from_stop_txt":unr.from_stop_txt,"unr_from_stop":unr.from_stop, "route":unr.route})


    # to stop index
    for pos, rd in enumerate(rdlist):
        if(rd.stop==to_stop):
            # for ring routes there will be two occurences of the stop, so we want the to_stop at the via-point and then we mirror the route
            if code == 'R' or code == '4': # for ring routes
                if from_stop==to_stop and pos==0:  # if first and last stop  are the same, then go to the second occurence
                    continue
                else:
                    to_index = rdlist.index(rd)
                    to_stop_found+=1           
                    break                                
            to_index = rdlist.index(rd)
            to_stop_found+=1           

            
    if to_stop_found>1:
        multiple_to_stops.append({"unr":unr,"count":to_stop_found,"to_stop":unr.to_stop})
        
    if to_stop_found == 0:
        print "To-Stop not found in Route Details for unr.id", unr.id , " unr.to_stop_txt=", unr.to_stop_txt
        mismatched_unrs['to'].append({"unr":unr,"unr_to_stop_txt":unr.to_stop_txt,"unr_to_stop":unr.to_stop, "route":unr.route})
       
    # indexes found , splice list
    rd_subset = rdlist[from_index:to_index+1]

    # if ring route, then mirror stops from the via-point
    if code == 'R' or code == '4':
        # ring specific code here. 
        # converts the given ring route subset to double size.
        # if ring route subset 
        #if not (unr.from_stop.id !=rdlist[0].stop.id and unr.to_stop.id !=rdlist[len(rdlist)-1]).stop.id:
        if not unr.is_full:       
            # if it is a subset of the full ring route, then routedetails
            rd_temp = copy.deepcopy(rd_subset)
            rd_temp.reverse()
            rd_subset.extend(rd_temp[1:])        
        else:
            # if full ring route, ignore splicing calculations and send route based only on "UP/DOWN" filtering
            return rdlist

    # by default, the route is ordered according to the up route so only check for down trips
    if not direction in ["UP", "up", "U"]:        
        rd_subset.reverse()
        prevdist= 0.0
        for pos, rd in enumerate(rd_subset):
            # if last stop is not a stage we still should assign the previous dist
            if rd.km or pos == len(rd_subset)-1:
                tempdist=rd.km
                rd.km=prevdist
                prevdist=tempdist                   
        
    # if route indexing is anything less than 5 or negative, then alert
    if (to_index - from_index) < 5:
        print "Route::",unr.route.code , "from pos", from_index, " to pos ", to_index
        badroutes.add(unr.route)

    return rd_subset

def check_route_and_rds():
    """
    because the full routedetails is given for the route, just a sanity check to make sure 
    route from/to stop ids match with the ones in the routedetails
  
    """

    lst = set()
    for r in Route.objects.all():
        rds = r.routedetail_set.all()
        if r.from_stop != rds[0].stop:
            lst.add(r)
        if  r.to_stop != rds[len(rds)-1].stop:
            lst.add(r)
    return lst

def get_non_ring_routes():
    """
    Gets routes which have unique routes which are ring route like but do not have that in route code
    """
    unr_lst = set()
    for unr in UniqueRoute.objects.all():        
        code = unr.route.code[3]
        if not (code == 'R' or code == '4'):
            if unr.from_stop==unr.to_stop:
                unr_lst.add(unr)
    return unr_lst

def get_non_ring_routes_via_rds():
    """
    Gets routes which have unique routes which are ring route like but do not have that in route code
    """
    route_lst = set()
    for r in Route.objects.all():        
        code = r.code[3]
#        if not (code == 'R' or code == '4'):
#            rds =  
#            if 
#                route_lst.add(unr.route)
    return route_lst
    

def get_bad_routes():
    """ 
    Gets a list of routes which have less than five routedetails or stops inany of their uniqueroutes.
    """
    bad_routes=set()
    for unr in UniqueRoute.objects.all():        
        rdlist = get_routedetail_subset(unr,"UP")
        if len(rdlist) < 5:
            bad_routes.add(unr.route)

        rdlist = get_routedetail_subset(unr,"DOWN")
        if len(rdlist) < 5:
            bad_routes.add(unr.route)
    return bad_routes

def make_is_full():
    fn=[]
    cn=[]
    for unr in UniqueRoute.objects.select_related().all():
        maxdist = max(unr.route.uniqueroute_set.values_list('distance'))[0]
        """
        if unr.distance==maxdist and not unr.is_full:
            unr.is_full=True
            unr.save()

        if unr.distance==unr.route.distance and not unr.is_full:
            unr.is_full=True
            unr.save()
        """
        # imp bug in BEST data, if the max_distance of the atlas entries do not
        # match the route.distance one of those is wrong
        if maxdist > unr.route.distance and unr.distance == maxdist:
            fn.append(unr)     
            cn.append(unr.route)

        if unr.distance==maxdist:            
            unr.is_full=True
            unr.save()
        else:
            unr.is_full=False
            unr.save()
    cn = list(set(cn))
     
    d = {"unrs": fn, "routes":cn}
    return d
            
                       
def runtime_in_minutes(schedule):
    """
    runtime returned is a single value and maybe would be more refined it would consider timespan.
    """
    
    runtime = schedule.runtime1 or schedule.runtime2 or schedule.runtime3 or schedule.runtime4

    tot=0.0
    cnt=0
    if schedule.runtime1:
        tot+=schedule.runtime1
        cnt+=1
    if schedule.runtime2:
        tot+=schedule.runtime2
        cnt+=1
    if schedule.runtime3:
        tot+=schedule.runtime3
        cnt+=1
    if schedule.runtime4:
        tot+=schedule.runtime4
        cnt+=1
    if cnt!=0:
        runtime = tot/cnt
        return runtime
        
    
    t_from, t_to = schedule.first_from, schedule.first_to
    if not t_from or not t_to:
        t_from, t_to = schedule.last_from, schedule.last_to
    return abs(t_from.hour * 60 + t_from.minute -
              (t_to.hour * 60 + t_to.minute))

def runtime_in_minutes_now(schedule):
    """
    runtime returned is a single value and maybe would be more refined it would consider timespan.
    """
    
    runtime = schedule.runtime1 or schedule.runtime2 or schedule.runtime3 or schedule.runtime4

    tot=0.0
    cnt=0
    if schedule.runtime1:
        tot+=schedule.runtime1
        cnt+=1
    if schedule.runtime2:
        tot+=schedule.runtime2
        cnt+=1
    if schedule.runtime3:
        tot+=schedule.runtime3
        cnt+=1
    if schedule.runtime4:
        tot+=schedule.runtime4
        cnt+=1
    if cnt!=0:
        runtime = tot/cnt
        return runtime
        
    
    t_from, t_to = schedule.first_from, schedule.first_to
    if not t_from or not t_to:
        t_from, t_to = schedule.last_from, schedule.last_to
    return abs(t_from.hour * 60 + t_from.minute -
              (t_to.hour * 60 + t_to.minute))

        
noLocsStops = []

def export_shapes():
    f = make_csv_writer("shapes.txt")
    f.writerow(["shape_id","shape_pt_lat","shape_pt_lon","shape_pt_sequence"])
    
    for road in Road.objects.all():
        ss = road.stop_set.all()
        # --FIXME  counter is giving a step count, stops however must be ordered by position in road before
        counter = 1
        for s in ss:
            if s.point:
                f.writerow(['road'+str(road.id),s.point.coords[1], s.point.coords[0],counter])
                counter+=1
            else:
                noLocsStops.append(s.__dict__)



stopset = set()

def export_stops(routelist):
    # stop_code is used for stop_id as its BEST specfic..
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
            # stop_code is used for stop_id as its BEST specfic
            if stop.point:
                f.writerow([str(stop.code),stop.name,stop.point.coords[1],stop.point.coords[0],str("Marathi:"+stop.name_mr+" Road:"+stop.road.name+" Area:"+stop.area.name+" Altnames:" )])
            
        except:
            print "error for writerow", stop.__dict__, stop.point.coords  
            #print "error: Stop id: %s, stop_code:%s " 


def route_diff(oldroutes,difflist):
    cr_from_codes = [Route.objects.get(code=a) for a in difflist]
    crset= set(cr_from_codes)
    oldroutes = set(oldroutes)
    oldroutes = oldroutes.difference(crset)
    return list(oldroutes)

def compare_unr_distances(routelist):
    rdict={}
    rdict["mismatch"]=[]
    for schedule, unr, route, direction, trip_id in generate_trips_unr():
        if route not in routelist: continue
        details =  get_routedetail_subset(unr, direction)

        # use interpolated distances
        #details = parseDistancesForDetails(details, parse_stages=True)

        # a lot of unique routes have a shorter distance than the main route even though they span its entire length
        dist1=0.0
        if unr.is_full and route.distance:
            dist1 = route.distance

        dist2 = unr.distance
        dist3=0.0
        for sequence, detail in enumerate(details):
            if detail.km:
                dist3+=float(detail.km)
                firststop_isstage=True if sequence == 0 else False
                laststop_isstage=True if sequence == (len(details)-1) else False
                
        schedule_info={"route_dist":dist1, "unr_dist":dist2, "routedetail_dist":dist3, "schedule":schedule.id}
        distance_mismatch = True if dist2 > dist3 and unr.is_full else False
        rdict[schedule.id]=schedule_info

        if distance_mismatch:
            rdict["mismatch"].append(schedule_info)

    return rdict
        
def getRoutesWBadRDs(cnt):
    routes = []
    for r in Route.objects.all():
        if r.routedetail_set.count() < cnt:
            routes.append(r)
    return routes

def export_stop_times2(routelist):
    f = make_csv_writer("stop_times.txt")
    f.writerow(["trip_id","arrival_time","departure_time","stop_id","stop_sequence"])
    
    for schedule, unr, route, direction, trip_id in generate_trips_unr():
        if route not in routelist: continue
        details = get_routedetail_subset(unr, direction)

        # use interpolated distances
        #details = parseDistancesForDetails(details, parse_stages=True)

        # calc avg speed for a trip. trip = unr+rs
        # 


        if unr.is_full and route.distance:
            dist1 = float(route.distance)

        # a lot of unique routes have a shorter distance than the main route even though they span its entire length
        dist2 = unr.distance


        dist3=0.0
        for seq, detail in enumerate(details):
            blankstops=0
            if detail.km:
                dist3+=float(detail.km)
                blankstops=0
            else:
                blankstops+=1
                if seq == len(details) - 1:
                    dist3+=float(0.3*blankstops)

        # dist2 is from unr, dist3 is got by traversing the routedetails
        dist = dist3

        #j runtime should be calculated for each separate runtime entry so stop_times becomes a bit more accurate.
        runtime = runtime_in_minutes(schedule)

        # if dist == 0.0 or runtime == 0
        nospeeds=0

        if not runtime > 0.0:
            avgspeed = dist/runtime   # in km/min         
        else:
            avgspeed = 12.0/60.0   # putting a default of 12 km/hour. 
            nospeeds+=1        

        initial_time = departure_time = schedule.first_to if direction in ["UP", "up", "U" ] else schedule.first_from

        if initial_time is None:
            initial_time = time_of("05:00:00")

        arrival_time = initial_time
        cumulative_distance = 0.0
        prev_at = arrival_time
        prev_dt = departure_time
        timedelta = 0
        distdelta = 0.0
        today = datetime.date.today()
        blankstops = 0
        prevstage = 0
        rdetails = []
        dt= 0
        for sequence, detail in enumerate(details):
            rdetails.append([sequence,detail])

        # main process 
        for sequence, detail in rdetails:
            stopset.add(detail.stop)
            # if stop is a stage, then it has km (delta) info
            if detail.km:
                cumulative_distance+=float(detail.km)
                #failsafe
                #if avgspeed<3.0/60.0:
                #    avgspeed=12.0/60.0

                offsettime = cumulative_distance/avgspeed
                dt = datetime.datetime.combine(today, initial_time) + datetime.timedelta(seconds=offsettime*60)
                arrival_time = dt.time()

                # Add 10 seconds to departure time 
                dt = datetime.datetime.combine(today, arrival_time) + datetime.timedelta(seconds=10) 
                departure_time = dt.time()                    

                f.writerow([trip_id,arrival_time.__str__().split(".")[0],departure_time.__str__().split(".")[0],str(detail.stop.code),sequence+1])

                prev_at = time_of(arrival_time.__str__().split(".")[0])
                prev_dt = time_of(departure_time.__str__().split(".")[0])                    
                blankstops=0
                prevstage = sequence
            else:
                # no km info, not a stage
                blankstops+=1
                # first stop
                if sequence == 0:
                    f.writerow([trip_id,initial_time,initial_time, str(detail.stop.code),sequence+1])
                elif sequence == len(details)-1:   
                    # if this is the last stop in the route, then          
                    offsettime = (cumulative_distance+(0.3*blankstops))/avgspeed
                    dt = datetime.datetime.combine(today, initial_time) + datetime.timedelta(seconds=offsettime*60)
                    arrival_time = dt.time()
                    dt = datetime.datetime.combine(today, arrival_time) + datetime.timedelta(seconds=60) 
                    departure_time =  dt.time()                    
                                            
                    #if prev_dt and time_of(arrival_time):
                    #    if time_of(arrival_time) < prev_dt:
                    #        arrival_time = "%02d:%02d:00" % (int((arrival+3)/60), (arrival+3) % 60)
                    #        departure_time=arrival_time

                    f.writerow([trip_id,arrival_time.__str__().split(".")[0],departure_time.__str__().split(".")[0],str(detail.stop.code),sequence+1])

                else:
                    # any other stop
                    f.writerow([trip_id,"","",str(detail.stop.code),sequence+1])

errlog = []
fastroutes =set()
slowroutes= set()

def convert_to_24h_time(dt):
    if isinstance(dt, datetime.time):
        if dt.hour <=2:
            m = dt.minute
            minutes = "0"+str(m) if len(str(m)) == 1 else str(m)
            s = dt.second
            seconds = "0"+str(s) if len(str(s)) == 1 else str(s)
            return str(24+dt.hour)+":"+minutes+":"+seconds
        else:
            return dt.__str__().split(".")[0]
    else:
        print("wrong input format")
        

def export_stop_times(routelist):
    print "Exporting stop times.."
    f = make_csv_writer("stop_times.txt")
    #f.writerow(["trip_id","arrival_time","departure_time","stop_id","stop_sequence", "cumulative_distance", "isStage"])
    f.writerow(["trip_id","arrival_time","departure_time","stop_id","stop_sequence"])
    
    # get trips and route details

    tooslows = 0
    toofasts = 0
    nospeeds=0
    rdlistempty=0
    
    print "Trips with faulty RDs::"    
    for schedule, unr, route, direction, trip_id in generate_trips_unr():

        if route not in routelist: continue
        #if not unr.is_full: continue

        #get route in sort_order based on UP or DOWN route 
        details =  get_routedetail_subset(unr, direction)

        # use interpolated distances
        #details = parseDistancesForDetails(details, parse_stages=True)

        if len(details) <= 4:
            print "rdlist not populated"   
            rdlistempty+=1
            badroutes.add(route)
            #continue

        #--------------------- get distance ---------------
       
        if unr.is_full and route.distance:
            dist1 = float(route.distance)

        # calc avg speed for a trip. trip = unr+rs

        dist2 = unr.distance
        
        # calculate distance based on route details
        dist3=0.0
        for seq, detail in enumerate(details):
            blankstops=0
            if detail.km and not seq ==0: # dont count the first stop's distance.
                dist3+=float(detail.km)
                blankstops=0
            else:
                blankstops+=1
                if seq == len(details) - 1:
                    dist3+=float(0.3*blankstops)

        dist = dist3

        #---------------------end get distance ---------------

        #--------------------- s ---------------

        runtime = runtime_in_minutes(schedule)  #j runtime should be calculated for each separate runtime entry, so stop_times becomes a bit more accurate.
        # if ring route, then double the runtime as runtime is calculated uptil the 'via' point.
        if str(route.code)[3]==4:
            runtime= int(2*runtime)

        #if dist == 0.0 or runtime == 0
        avgspeed = 12.0/60.0
        if not runtime == 0.0:
            avgspeed = dist/runtime   # in km/min         
        else:
            # putting a default of 12km/hour. 
            #avgspeed = 12.0/60.0  
            nospeeds+=1                

        # checks and failsafes            
        if avgspeed < 5.0/60.0:
            #avg human walking speed is 5 km/hr
            print "Slow: Trip: %s::Speed: %.2f, Dist:(route: %s, unr: %s, rd: %s) ,run_time: %s,  stops: %s" %(trip_id, avgspeed*60.0, dist1, dist2, dist3, str(runtime), str(len(details))) 
            slowroutes.add(route)
            tooslows+=1

        if avgspeed > 40.0/60.0:
             print "Fast: Trip: %s::Speed: %.2f, Dist:(route: %s, unr: %s, rd: %s) ,run_time: %s,  stops: %s" %(trip_id, avgspeed*60.0, dist1, dist2, dist3, str(runtime), str(len(details))) 
             toofasts+=1
             fastroutes.add(route)
            #avgspeed=30.0/60.0
        
        # setting up some vars and failsafes
        initial_time = departure_time = schedule.first_to if direction == "UP" else schedule.first_from
        if initial_time == datetime.time(0,0,0):
            initial_time  = time_of("05:00:00")

        arrival_time = initial_time
        cumulative_distance = 0.0
        prev_at = initial_time
        prev_dt = initial_time
        timedelta = 0
        distdelta = 0.0
        today = datetime.date.today()
        blankstops = 0
        prevstage = 0
        rdetails = []
        dt= 0
        for sequence, detail in enumerate(details):
            rdetails.append([sequence,detail])

        # main process 
        for sequence, detail in rdetails:
            stopset.add(detail.stop)
            # if stop is a stage, then it has km (delta) info
            if detail.km  and sequence!=0: # dont add the first stops distance even if its a stage
                cumulative_distance+=float(detail.km)

                if avgspeed != 0.0:
                    offsettime = cumulative_distance/avgspeed
                    dt = datetime.datetime.combine(today, initial_time) + datetime.timedelta(seconds=offsettime*60)
                    arrival_time = dt.time()
                    at_str = convert_to_24h_time(arrival_time) #arrival_time.__str__()
                    #pdb.set_trace()
                    # Add 10 seconds to departure time 
                    dt = datetime.datetime.combine(today, arrival_time) + datetime.timedelta(seconds=10)
                    departure_time = dt.time()
                    
                    dt_str = convert_to_24h_time(departure_time) #arrival_time.__str__().split(".")[0]                    
                    
                    #f.writerow([trip_id, str(detail.stop.code),sequence+1,cumulative_distance, detail.stage ])
                    if time_of(at_str) and prev_dt and time_of(at_str) < prev_dt:
                        dt = datetime.datetime.combine(today, initial_time) + datetime.timedelta(seconds=offsettime*60+30)
                        arrival_time = dt.time()
                        at_str = convert_to_24h_time(arrival_time) #arrival_time.__str__()
                        

                    f.writerow([trip_id,at_str,dt_str,str(detail.stop.code),sequence+1])

                    prev_at = time_of(arrival_time.__str__().split(".")[0])
                    prev_dt = time_of(departure_time.__str__().split(".")[0])                    

                    blankstops=0
                    prevstage = sequence
                    
            else:
                # for non-stage stops
                # go to the next stage, get no. of stops in the middle, get the km delta, 
                blankstops+=1

                # first stop
                if sequence == 0:
                    f.writerow([trip_id,convert_to_24h_time(initial_time),convert_to_24h_time(initial_time),str(detail.stop.code),sequence+1])
                    #f.writerow([trip_id,initial_time,initial_time,str(detail.stop.code),sequence+1,cumulative_distance, detail.stage ]) 

                else:    
                # if this is the last stop in the route, then             
                    if sequence == len(details) - 1:
                        offsettime = (cumulative_distance+(0.3*blankstops))/avgspeed
                        dt = datetime.datetime.combine(today, initial_time) + datetime.timedelta(seconds=offsettime*60)
                        arrival_time = dt.time()
                        at_str = convert_to_24h_time(arrival_time)
                        #dt = datetime.datetime.combine(today, arrival_time) + datetime.timedelta(seconds=60) 
                        departure_time = dt.time()                    
                        dt_str = convert_to_24h_time(departure_time) #arrival_time.__str__().split(".")[0]              
                        #arrival = initial_time.hour * 60 + initial_time.minute + runtime_in_minutes(schedule) + 7
                        #arrival_time = "%02d:%02d:00" % (int(arrival/60), arrival % 60)                        
                        #departure_time = "%02d:%02d:00" % (int(arrival/60), arrival % 60)                    

                        if prev_dt and time_of(arrival_time):
                            if time_of(arrival_time) < prev_dt:
                                arrival_time = "%02d:%02d:00" % (int((arrival+3)/60), (arrival+3) % 60)
                                departure_time=arrival_time
                                at_str = convert_to_24h_time(time_of(arrival_time))
                                dt_str = convert_to_24h_time(time_of(arrival_time))

                        f.writerow([trip_id,
                                    at_str,
                                    dt_str,
                                    str(detail.stop.code),sequence+1])

                        #f.writerow([trip_id,arrival_time,departure_time,str(detail.stop.code),sequence+1,cumulative_distance, detail.stage ])
                        
                    else:
                        # if any other stop
                        f.writerow([trip_id,"","",str(detail.stop.code),sequence+1])
                        #f.writerow([trip_id,"","",str(detail.stop.code),sequence+1,cumulative_distance, detail.stage ])
                


    print "Trips too fast::", toofasts 
    print "Trips too slow::", tooslows 
    print "Trips with no speeds", nospeeds

    print "Exporting stop times done."
                                
        #-----------------------------------------------------------------------------------


    """

    # if this is the last stop in the route, then 
    if sequence == len(details) - 1:
        arrival = initial_time.hour * 60 + initial_time.minute + runtime_in_minutes(schedule)
        arrival_time = "%02d:%02d:00" % (int(arrival/60), arrival % 60)
        f.writerow([trip_id,arrival_time,departure_time,detail.stop.code,sequence])
    else:
        departure_time = ""
        f.writerow([trip_id,arrival_time,departure_time,detail.stop.code,sequence])
    """

    #routelist = getRoutesHavingAllLocs()    

    #1. get routeDetails
    #2. get unique routes as unr and the routeDetails subset as rd_subset for that uniqueroute
    #3. get all unr.routeschedules as unr.rs 
    #4. get total distance as tdist from rd_subset
    #5. get runtime from unr.rs 
    #6. get_runtime()
    #7. avgspeed = tdist/runtime... if runtime is not available then ??
    #8.  


    """   # old code just for fallback
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
stop_times.txt   - algo for old code
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

def time_of(timestr):
    try:
        tm = timestr.split(":")
        return datetime.time(int(tm[0]),int(tm[1]),int(tm[2]))
    except:
        return None


def parseDistancesForDetails(details, parse_stages):
    """
    This parses a set of route details having intermediate distances and interpolates them. 
    parse_stages(bool) denotes if the stage itself is to be parsed and replaced.
    returns the list of details with parsed info.
    """    
    prevstage=-1    
    for seq, detail in enumerate(details):        
        # dont calculate for first stop
        if seq==0:continue
        
        if detail.stage:
            prevstage = seq
            # if the first stop hasnt been given km, and if its the first stop, don't make a change, else set the km to prev value.)
            if  seq > 0 and parse_stages:
                if details[seq-1].km > 0.0 and not details[seq-1].stage:
                    detail.km = details[seq-1].km
        else:            
            blankstops=0
            distdelta=0.0
            for d in details[prevstage+1:]:
                if d.stage:
                    #prevstage = seq
                    if blankstops!=0:
                        distdelta=d.km/(blankstops+1)    
                        break
                    else:
                        # if 1st stop is a stage                       
                        distdelta=d.km
                        break
                else: 
                    # make sure first stop doesnt come in the count, as 
                    #if seq > 0:
                    blankstops+=1        
            
                # if last stop is reached while traversing
                if details.index(d) == len(details)-1:
                    # if the last stop is not a stage, then we dont have measure of distance, so use  a default of .3km per stop distance
                    distdelta = 0.3*blankstops
                    break
            
            detail.km = distdelta

        #print("d: %d, serial: %s , dist: %f , stage: %s" %(detail.id, detail.serial, detail.km, detail.stage))
    return details

def parseDistancesForAllRoutes():
    for r in Route.objects.all():
        details = list(RouteDetail.objects.filter(route=r))
        parsed = parseDistancesForDetails(details, False)
        for d in parsed:
            d.save()
        
def export_frequencies(routelist):
    f = make_csv_writer("frequencies.txt")
    """
    EACH ROW IN FREQUENCIES
    - For an entry in atlas, [ i.e. a given trip+service_id [subset + schedule days] ] 
    If there are headway timings for diff time slots, eg. 
    h7-11, h11-16, h16-22,h22-25
    
    then
    """
    TIMESPANS = ((None,"06:59:59"),
                 ("07:00:00","10:59:59"),
                 ("11:00:00","16:59:59"),
                 ("17:00:00","19:59:59"),
                 ("20:00:00",None))
    
    f.writerow(["trip_id", "start_time","end_time","headway_secs"])
    for schedule, unr, route, direction, trip_id in generate_trips_unr():
        # inclusion criteria
        if route not in routelist: continue
        runtime = runtime_in_minutes(schedule)
        if runtime <= 0.0 or  unr.distance is None or unr.distance == 0.0: continue     
 
        
        headway = (schedule.headway1,
                   schedule.headway2,
                   schedule.headway3,
                   schedule.headway4,
                   schedule.headway5)

        ts_start = ""
        timespanchange = False

        for span, (start_time, end_time) in enumerate(TIMESPANS):
            # getting headway timings
            # making sure the start_time is earlier than the end_time 
            # making start and end as datetime.time                
            # check if previous 
            if timespanchange:
                start_time = ts_start
                timespanchange = False

            if direction == "UP":
                """
                # if 'up' then take *_from values else take *_to values from schedule
                if start_time is None:
                    start_time = schedule.first_from.__str__()
                if end_time is None:                    
                    end_time = schedule.last_from.__str__()

                   """

                if start_time is None:
                    if schedule.first_from:
                        start_time = schedule.first_from.__str__()
                    else:
                        start_time = "05:00:00" # magic number here in case BEST data isnt found             

                if end_time is None:
                    if schedule.last_from:
                        end_time = schedule.last_from.__str__()
                    else:
                        end_time = "22:59:59" # magic number here in case BEST data  isnt found 


                    """
                # if base values are null then put default values                
                if schedule.first_from == datetime.time(0,0,0)
 and start_time is None:
                    start_time = "05:00:00" # magic number here in case BEST data isnt found             
                if schedule.last_from == datetime.time(0,0,0):
                    end_time = "22:59:59" # magic number here in case BEST data  isnt found 
                # check if start_time is always earlier than end_time.. this needs to be logged soon!
                if time_of(start_time) >= time_of(end_time):
                    start_time = "05:00:00" 
                if time_of(end_time) <= time_of(start_time):
                    end_time = "22:59:59" 
                    """
            else:    
                if start_time is None:
                    if schedule.first_to:
                        start_time = schedule.first_to.__str__()
                    else:
                        start_time = "05:00:00" # magic number here in case BEST data isnt found             

                if end_time is None:
                    if schedule.last_to:
                        end_time = schedule.last_to.__str__()
                    else:
                        end_time = "22:59:59" # magic number here in case BEST data  isnt found 
 

                    """
                if start_time is None: 
                    start_time = schedule.first_to.__str__()
                if end_time is None:
                    end_time = schedule.last_to.__str__()

                # if base values are null then put default values                
                if schedule.first_from == datetime.time(0,0,0):
                    start_time = "05:00:00" # magic number here in case BEST data isnt found             
                if schedule.last_from == datetime.time(0,0,0):
                    end_time = "22:59:59" # magic number here in case BEST data  isnt found 
                # check if start_time is always earlier than end_time.. this needs to be logged soon!
                if  time_of(start_time) >= time_of(end_time):
                    start_time = "05:00:00" # magic number here in case BEST data isnt found
                if  time_of(end_time) <= time_of(start_time):
                    end_time = "22:59:59" # magic number here in case BEST data isnt found
                    """
            if headway[span] is not None:
                # if ff > end_time,drop headway 
                if time_of(start_time) < time_of(end_time):
                    f.writerow([trip_id, start_time, end_time, headway[span]*60])
                else:
                    # if the start_time is later than the end_time  of the first timespan, then change the start_time of the second timespan
                    timespanchange = True
                    ts_start = start_time





def export_frequencies2(routelist):
    f = make_csv_writer("frequencies.txt")
    """
    EACH ROW IN FREQUENCIES
    - For an entry in atlas, [ i.e. a given trip+service_id [subset + schedule days] ] 
    If there are headway timings for diff time slots, eg. 
    h7-11, h11-16, h16-22,h22-25
    
    then
    """
    TIMESPANS = (("05:00:00","06:59:59"),
                 ("07:00:00","10:59:59"),
                 ("11:00:00","16:59:59"),
                 ("17:00:00","19:59:59"),
                 ("20:00:00","23:59:59"))
    
    f.writerow(["trip_id", "start_time","end_time","headway_secs"])
    for schedule, unr, route, direction, trip_id in generate_trips_unr():
        # inclusion criteria
        if route not in routelist: continue        
        runtime = runtime_in_minutes(schedule)
        if runtime <= 0.0 or unr.distance is None or unr.distance == 0.0: continue     

        headway = (schedule.headway1,
                   schedule.headway2,
                   schedule.headway3,
                   schedule.headway4,
                   schedule.headway5)

        # to indicate if time represents the next day eg. 02:00:00 am
        lf_overflow = False
        lt_overflow = False

        for span, (start_time, end_time) in enumerate(TIMESPANS):
            # getting headway timings

            # making start and end as datetime.time                
            st = time_of(start_time)
            et = time_of(end_time)
            ff = schedule.first_from
            lf = schedule.last_from
            ft = schedule.first_to
            lt = schedule.last_to

            # sanity checks for these times to be applied here.. like if ff is given and ft is not, then ft is ff+runtime, etc

            if ff is None:
                ff=time_of("05:00:00")

            if lf is None:
                lf=time_of("23:59:59")        

            if ft is None:
                ft=time_of("05:00:00")

            if lt is None:
                lt=time_of("23:59:59")


            try:
                # check for any end_times going beyond 00:00:00 and make into 23:59:59,
                # add 24:00:00 + offset at time of writing to file
                # for comparison use 23:59:59. so any time span beyond that needs a custom operator for times.
                
                if schedule.last_from < schedule.first_from:
                    lf = time_of("23:59:59")
                    lf_overflow = True
                if schedule.last_to < schedule.first_to:
                    lt = time_of("23:59:59")
                    lt_overflow = True
            except:
                print "time comparison error "
                pass



            if direction == "UP":
                """
                # if 'up' then take *_from values else take *_to values from schedule
                """

                # any time interval [(ff,lf),(ft,lt)] is defined by its end points ,
                # so basic algo is to check if the endpoint lies b4, in or after the timespan
                
                # for ff
                # b4
                if ff < st:
                    if span == 0:
                        st = ff

                # in
                if st < ff and ff < et:
                    st=ff

                # aft
                if ff > et:
                    continue
                        

                # for lf
                # b4                 
                if lf < st:
                    continue
                
                # in
                if st < lf and lf < et:
                    et = lf #!  lf
                
                # aft, if span is last then extend
                if et < lf:
                    if span ==  len(TIMESPANS) -1:
                        et = lf 


                if headway[span]:
                    # convert to string
                    st_str = st.__str__().split(".")[0]
                    et_str = et.__str__().split(".")[0]

                    # adjusting overflows 
                    if lf_overflow and span == len(TIMESPANS) -1:
                        lf_time = schedule.last_from.hour * 60 + schedule.last_from.minute
                        et_str = "%02d:%02d:00" % (int(lf_time/60)+24, lf_time % 60)
                        lf_overflow = False
                        

                    f.writerow([trip_id,st_str, et_str, headway[span]*60])                
                
            else:    

                # for down, ft
                # b4
                if ft < st:
                    if span == 0:
                        st = ft
                # in
                if st < ft and ft < et:
                    st=ft

                # aft
                if ft > et:
                    continue                


                # for lt
                # b4                 
                if lt < st:
                    continue
                
                # in
                if st < lt and lt < et:
                    et = lt
                
                # aft
                if et < lt:
                    # for last timespan
                    if span ==  len(TIMESPANS) -1:
                        et = lt

                if headway[span]:

                    # convert to string
                    st_str = st.__str__().split(".")[0]
                    et_str = et.__str__().split(".")[0]

                    # adjusting overflows                         
                    if lt_overflow and span == len(TIMESPANS) -1:
                        lt_time = schedule.last_to.hour * 60 + schedule.last_to.minute
                        et_str = "%02d:%02d:00" % (int(lt_time/60)+24, lt_time % 60)
                        lt_overflow = False
                                        
                    f.writerow([trip_id,st_str, et_str, headway[span]*60])

def export_stops_from_set():
    import codecs
    f =codecs.open(join(PROJECT_ROOT, "gtfs", "gtfs_mumbai_bus", "stops.txt"), "w", "utf-8")
    f.write("stop_id,stop_name,stop_lat,stop_lon,stop_desc\n")

    for stop in stopset:
        # stop_code is used for stop_id as its BEST specfic
        desc = "Marathi:"+stop.name_mr+" Road:"+stop.road.name+" Area:"+stop.area.name

        alt_names = [an.name for an in stop.alt_names.all()]
        alt_name_str = " Altnames:"        
        for an in alt_names:
            alt_name_str+= an + "; "
        # remove trailing delimiter and space
        alt_name_str=alt_name_str[:-2]
        if alt_names:
            desc+=alt_name_str

        
        f.write(str(stop.code) + "," + stop.name.replace(",","") +"," +  str(stop.point.coords[1]) +"," + str(stop.point.coords[0]) +"," +  desc.replace(",","") + "\n") 



def makeStopList():
    import codecs
    f =codecs.open(join(PROJECT_ROOT, "../db_csv_files", "MarathiStopsLeft.csv"), "w", "utf-8")
    f.write("stop_id\tstop_code\tstop_name\tmarathi_name\n")

    for s in Stop.objects.all():
        if s.name_mr in ('', None):
            s.name_mr= ''
            line = str(s.id) +"\t"+ str(s.code)+"\t" + str(s.name) + "\t" + s.name_mr
            f.write(line+ "\n")

    f.close()

#def readStopList():
    

def get_rd_distance(unr,addextradist):
    """
    Sums up the distances for a given route. 
    Also adds 300 mts. for each stop for calculating the last stop, 
    if it doesnt have distance info. (This is for the trip times)
    def get_rd_distance(UniqueRoute unr, bool addextradist):
    """
    details= RouteDetail.objects.filter(route=unr.route).order_by('serial')
    dist =0.0
    for seq, detail in enumerate(details):
        blankstops=0
        if detail.km:
            dist+=float(detail.km)
            blankstops=0
        else:
            blankstops+=1
            if seq == len(details) - 1:
                if addextradist:
                    dist+=float(0.3*blankstops)
                
    return dist

def routes_nonstage_last_stop():
    for r in Route.objects.all():
        if r.uniqueroute_set.all():
            unr = r.uniqueroute_set.all()[0]
            if g.get_rd_distance(unr,0) != g.get_rd_distance(unr,1):
                cnt.append(r)

    return cnt
                
def export_atlas():    
    import codecs
    f =codecs.open(join(PROJECT_ROOT, "gtfs", "recomputed_atlas.csv"), "w", "utf-8")

    f = csv.writer(open(join(PROJECT_ROOT, "gtfs", "gtfs_mumbai_bus", "recomputed_atlas.csv"), "w"), delimiter="\t", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    f.writerow(["RouteCode","RouteAlias","BusesAM","BusesNoon","BusesPM","BusType","Depot","FromStopCode","FromStopName","FromStopOriginal","FromStopMarathi", "FirstFrom","LastFrom","ToStopCode","ToStopName","ToStopOriginal","ToStopMarathi","FirstTo","LastTo","rt1","rt2","rt3","rt4","headway1","headway2","headway3","headway4","headway5","ScheduleType","RouteSpan/AtlasDistance", "DistanceMasterRoute", "DistanceRouteDetail", "mismatchedfromstop","mismatchedtostop","DaysOfRun" ])
    for unr in UniqueRoute.objects.all().order_by("route__code"):
        for rs in unr.routeschedule_set.all().order_by("schedule_type"):
            bus_type= RouteType.objects.get(code=str(unr.route.code)[3]).faretype 
            rd_dist=get_rd_distance(unr,0)
            
            f.writerow([
                    unr.route.code, 
                    unr.route.alias, 
                    rs.busesAM,
                    rs.busesN,
                    rs.busesPM,
                    bus_type,
                    rs.depot_txt,
                    unr.from_stop.code,
                    unr.from_stop.name.title(),
                    unr.from_stop_txt,
                    unr.from_stop.name_mr.encode('utf-8'),
                    rs.first_from,
                    rs.last_from, 
                    unr.to_stop.code, 
                    unr.to_stop.name.title(),
                    unr.to_stop_txt,
                    unr.to_stop.name_mr.encode('utf-8'), 
                    rs.first_to, 
                    rs.last_to, 
                    rs.runtime1,rs.runtime2,rs.runtime3,rs.runtime4,
                    rs.headway1,rs.headway2,rs.headway3,rs.headway4,rs.headway5, 
                    rs.schedule_type,
                    unr.distance,
                    unr.route.distance,
                    rd_dist,
                    1 if 70 > fuzzprocess.ratio(unr.from_stop.name.lower(),unr.from_stop_txt.lower()) else 0,
                    1 if 70 > fuzzprocess.ratio(unr.to_stop.name.lower(),unr.to_stop_txt.lower()) else 0,
                    SCHED[rs.schedule_type].__str__().strip('[]')
                    ])
 


def fire_up(routelist):
    if not routelist:
        routelist = getCompleteRoutes2()
    export_feed_info()
    export_routes(routelist)
    export_frequencies2(routelist)
    export_stop_times(routelist)
    #export_stops(routelist)
    export_stops_from_set()
    export_calendar()
    export_trips(routelist)
    export_agency()
    

