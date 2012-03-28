from mumbai.models import *
import csv
from settings import PROJECT_ROOT
from os.path import join
import json
import datetime
import sys
from django.contrib.gis.geos import Point
from imports.import_atlas import getFromToStopsForRoute, importUniqueRoutes
from imports import postload_cleanup as postclean
from decimal import Decimal

globalerr = []

def RouteType_save(entry):
    obj = RouteType(code=entry[0], rtype=entry[1], faretype=entry[2])
    obj.save()
    #print obj.__dict__ 

def getFromToStopsFromRouteDetails(code):
    routeDetails = RouteDetail.objects.filter(route_code=code).order_by('serial')
    if routeDetails.count() == 0:
        return None
    fromStop = routeDetails[0].stop
    toStop = routeDetails[routeDetails.count() -1].stop
    return (fromStop, toStop,)

def Route_save(entry):        
    """
    try:
        f_stop = Stop.objects.filter(name=str(entry[2]))[0]
    except IndexError:
        f_stop = None 

    try:
        t_stop = Stop.objects.filter(name=str(entry[3]))[0]
    except IndexError:
        t_stop = None 
    """
    from_to = getFromToStopsFromRouteDetails(entry[0])
    if from_to is None:
        globalerr.append({"data" :entry[0], error:["Route not found"]})

       #obj = Route(code=entry[0], alias=entry[1], from_stop_txt=entry[2], to_stop_txt=entry[3], from_stop=from_to[0], to_stop=from_to[1], distance=Decimal(entry[4]), stages=int(entry[5]))

    
    obj = Route(
        code=str(entry[0]), 
        alias=str(entry[1]), 
        from_stop=from_to[0],
        from_stop_txt=str(entry[2]), 
        to_stop_txt=str(entry[3]), 
        to_stop=from_to[1],
        distance=Decimal(entry[4]), 
        stages=int(entry[5])) 
    obj.save()

    # throw an error if the stops mapped do not exist.
    # but load nulls into db anyway
    # IndexError implies that nothing was mapped.
    # MultipleRows found indicates ambiguity when there should'nt be.

   

    #f_stop = Stop.objects.get(name=str(entry[2]))[0]
    #t_stop = Stop.objects.get(name=str(entry[3]))[0]
    
    #print obj.__dict__ 

def HardCodedRoute_save(entry):
    obj = HardCodedRoute(code=str(entry[0]), alias=entry[1], faretype=entry[2])
    obj.save()
    #print obj.__dict__ 

def Depot_save(entry):
    obj = Depot(
        code=str(entry[0]),
        name=str(entry[1]), 
        stop=int(entry[2])
        ) 
    obj.save()
    #print obj.__dict__  

def Holiday_save(entry):
    date_format = entry[0].rsplit('.')
    theday = int(date_format[0])
    themonth = int(date_format[1])
    theyear = int('20'+ date_format[2])
    obj = Holiday(date=datetime.date(day=theday, month=themonth, year=theyear), name=str(entry[1])) 
    obj.save()
    #print obj.__dict__  

def RouteDetail_save(entry):

    temp_stop=Stop.objects.get(code=int(entry[2])) 
    """try:
        temp_route=Route.objects.get(code=str(entry[0]))
    except:
        temp_route=None
    try:
        temp_stop=Stop.objects.get(code=int(entry[2])) 
    except:
        temp_stop=None
    """
    obj = RouteDetail(
        route_code = entry[0],
        route = None,
        serial=int(entry[1]), 
        stop= temp_stop,
        stage=(lambda:entry[3].startswith('1'), lambda:None)[ entry[3] == '' ](), 
        km=(lambda:None,lambda:Decimal(entry[4]))[ entry[4] != '' ]())
    obj.save()
    #print obj.__dict__  
       
def Road_save(entry):
    obj = Road(code=int(entry[0]), name=str(entry[1])) 
    obj.save()
    #print obj.__dict__
  
def Fare_save(entry):
    obj = Fare(
            slab=Decimal(entry[0]), 
            ordinary=int(entry[1]), 
            limited=int(entry[2]), 
            express=int(entry[3]), 
            ac=int(entry[4]), 
            ac_express=int(entry[5])
            ) 
    obj.save()
    #print obj.__dict__
   
def Area_save(entry):
    obj = Area(code=int(entry[0]), name= str(entry[1])) 
    obj.save()
    #print obj.__dict__    

def Stop_save(entry):
    
    _road = Road.objects.get(code=int(entry[4]))
    _area = Area.objects.get(code=int(entry[5]))
    try:
        _depot = Depot.objects.filter(code=str(entry[6]))[0]
    except IndexError:
        _depot = None 

    obj = Stop(
        code=int(entry[0]), 
        name=str(entry[1]), 
        dbdirection=str(entry[2]), 
        chowki=(entry[3]).startswith('TRUE'),
        road=_road,
        area=_area,
        depot=_depot
        ) 

    obj.save()
    #print obj.__dict__

# There is no model as StopMarathi/AreaMarathi, but this is done to separate errors arising from different files, and also that the Marathi names should be done after the Stop and Area entities have been fully loaded cuz thats how we get them from BEST.

def StopMarathi_save(entry):
    obj = Stop.objects.get(code=int(entry[0])) 
    obj.name_mr = unicode(entry[1], 'utf-8')
    obj.save()
    #print obj.__dict__  

def AreaMarathi_save(entry):
    obj = Area.objects.get(code=int(entry[0])) 
    obj.name_mr = unicode(entry[1], 'utf-8')
    obj.save()
    #print obj.__dict__  

loc1s = 0
loc2s = 0

class NoPointsFoundError(Exception):
    pass

def StopLocation_save(entry):
    this_stop = Stop.objects.get(code=int(entry[4]))
    
    #hits = {'one':[],'two':[],'three':[],'four':[]}

    flagerr = 0

    if entry[0] and entry[1]:
        loc1 = StopLocation(stop=this_stop, point=Point(float(entry[1]), float(entry[0])),direction='U' )
        loc1.save()
        #loc1s+=1
    else:
        flagerr=1

    if entry[2] and entry[3]:
        loc2 = StopLocation(stop=this_stop, point=Point(float(entry[3]), float(entry[2])),direction='D' )
        loc2.save()                                
        #loc2s+=1
    else:
        flagerr+=1

    if flagerr == 2:
        flagerr = 0
        raise NoPointsFoundError

    #print "Loc1s found : ", loc1s
    #print "Loc2s found : ", loc2s



saveorder = ["Fare","Holiday","Area","Road","Depot","Stop", "StopMarathi","AreaMarathi","RouteDetail", "Route","RouteType","HardCodedRoute","StopLocation" ]

mappingtosave = {
    "Fare":Fare_save,
    "Holiday":Holiday_save,
    "Area":Area_save,
    "Road":Road_save,
    "Stop":Stop_save,
    "Depot":Depot_save,
    "RouteDetail":RouteDetail_save,
    "Route":Route_save,
    "RouteType":RouteType_save,
    "HardCodedRoute":HardCodedRoute_save,
    "StopMarathi":StopMarathi_save,
    "AreaMarathi":AreaMarathi_save,
    "StopLocation":StopLocation_save
# There is no model as StopMarathi/AreaMarathi, but this is done to separate errors arising from different input files.
    
}

def loadFKinRouteDetail():
    err=[]
    good_saves = 0
    print "\nLoading foreign keys into Route Details ... "
    for rd in RouteDetail.objects.all():
        try:
            rd.route=Route.objects.get(code=rd.route_code)
            rd.save()
            good_saves+=1
        except:
            rd.route=None
            err.append({"data":rd.route_code, "error":["Route Not Found in Route"]})

    #errors = open(join(PROJECT_ROOT, "../errors/RouteNotFoundErrors.json"), "w")
    size = len(err)
    print "No. of Routes in RouteDetail mapped to Route: " , str(good_saves)
    print "No. of Routes in RouteDetail not mapped to Route: " , str(size)

    if (size != 0) :
        print "See /errors/RouteNotFoundErrors.json for details"
        
    #errors.write(json.dumps(err, indent=2))
    #errors.close()
    return err



def CsvLoader(thismodel):
    try:
        CsvFile = csv.reader(open(join(PROJECT_ROOT, "../db_csv_files/"+thismodel+ ".csv"), "r"), delimiter="\t")
    except:
        print "Error opening file. Please check if ", thismodel," file exists and you have read/write permissions. Input files should be tab delimited, not comma delimited."
        exit()
    globalerr =[]

    #f.write("Data" + '\t' + "Error thrown" + '\n')

    header = CsvFile.next()
    print "\nLoading " + thismodel + "s..."
    print "Fields: ", header
    if ( header[0].find(',') != -1 ):
       print thismodel + "input file should be tab delimited, not comma delimited!"
       return
    errcount=0
    for entry in CsvFile:
        try:          
            #get the function for this model
            object_save = mappingtosave[thismodel]
            object_save(entry)
        except:
            globalerr.append({"data":str(entry), "error":str(sys.exc_info())})
            errcount+=1; 
            #print "Error:", str(entry) + '\t' +  str(sys.exc_info()[0]) + '\n'

    errors = open(join(PROJECT_ROOT, "../errors/"+ thismodel + "Errors.json"), 'w')
    errors.write(json.dumps(globalerr, indent=2))
    errors.close()


    DataLinesInFile = CsvFile.line_num -1
    stats = str(DataLinesInFile - errcount ) + " " +  thismodel + "s loaded without errors. Number of Errors encountered: " + str(errcount) + ". "
    if errcount > 0 :
        stats+="See " +  thismodel + "Errors.json file for details."
    print stats
    return

def fire_up():
    for model in saveorder:
        CsvLoader(model)

    loadFKinRouteDetail()
    
    # also
    importUniqueRoutes()    
    print "loading UniqueRoute..."
    #postclean.copydefaultStopLocations()
    postclean.copynames2display_name()
    
#----------------------------------------------------------

"""
RouteTypes
data changed
5	Rind Limited	LTD
to
5	Ring Limited	LTD
9	A/C Exp Ext	ACEXP
to
9	AC Exp Ext	ACEXP



test = CsvFile.next()
print test



CsvFile = csv.reader(open("/home/johnson/Desktop/chaloBEST/db_csv_files/AreaMaster.csv", "r"))
CsvFile.next()
for entry in CsvFile:
    obj = AreaMaster(int(entry[0]), entry[1]) 
    obj.save()



for line in f.readlines():
  if str(line) not in slist:
  slist.append(str(line))

Different Shedule entries in atlas:
['MS', 'HOL', 'SUN', 'MF&HOL', ' ', 'SAT', '', 'MF', 'SH', 'AD', 'SAT&SUN', 'MS&HOL', 'FW', 'SAT/SH', 'FH', 'SAT&HOL', 'SAT&SH', 'SAT/SUND&HOL', 'S/H', 'SAT,SUN&HOL', '2nd &4th']

DAYS = {
1: 'Monday',
2: 'Tuesday',
3: 'Wednesday',
4: 'Thursday',
5: 'Friday',
6: 'Saturday',
7: 'Sunday',
8: 'Holiday'
}

SCHED = 
{'MS':[1,2,3,4,5,6], 
 'HOL':[8], 
 'SUN':[7], 
 'MF&HOL':[1,2,3,4,5,8],  
 'SAT':[6], 
 'MF':[1,2,3,4,5], 
 'SH':[7,8], 
 'AD':[1,2,3,4,5,6,7,8], 
 'SAT&SUN':[6,7], 
 'MS&HOL':[1,2,3,4,5,6,8], 
 'FW':[1,2,3,4,5,6,7], 
 'SAT/SH':[6,7,8], 
 'FH':['???'], 
 'SAT&HOL':[6,8], 
 'SAT&SH':[6,7,8], 
 'SAT/SUND&HOL':[6,7,8], 
 'S/H':[7,8], 
 'SAT,SUN&HOL':[6,7,8], 
 '2nd &4th':['???']
}


}

In Atlas:

SPL-1		8	6	7	DD	CD	Chh.Shivaji Terminus	8.15	18.53	N.C.P.A.	8.30	19.05	5.8	25	27	32		 --	3	6	4	 ---	Chh.Shivaji Terminus	20	2nd &4th



StopMaster
2312	OM NGR.(WARE HOUSE)		0	0	3	MLD
changed to 
2312	OM NGR.(WARE HOUSE)		0	29	3	MLD


3899	DAVA BAZAR(KALBADEVI)		0	641	0	CD
changed to 
3899	DAVA BAZAR(KALBADEVI)		0	641	150	CD


4379	CRISIL HOUSE	U	0	229	0	VKD
changed to
4379	CRISIL HOUSE	U	0	229	118	VKD


4551	SAFED POOL	U	0	374	0	KLD
changed to 
4551	SAFED POOL	U	0	374	170	KLD




AreaCsv = csv.reader(open("/home/johnson/Desktop/chaloBEST/db_csv_files/AreaMaster.csv", "r"))
AreaCsv = csv.reader(open("/home/johnson/Desktop/chaloBEST/db_csv_files/AreaMaster.csv", "r"))
AreaCsv = csv.reader(open("/home/johnson/Desktop/chaloBEST/db_csv_files/AreaMaster.csv", "r"))
AreaCsv = csv.reader(open("/home/johnson/Desktop/chaloBEST/db_csv_files/AreaMaster.csv", "r"))
AreaCsv = csv.reader(open("/home/johnson/Desktop/chaloBEST/db_csv_files/AreaMaster.csv", "r"))
"""
