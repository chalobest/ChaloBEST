from mumbai.models import *
import csv
from settings import PROJECT_ROOT
from os.path import join
import json
import datetime
import sys

def AreaLoader():
    CsvFile = csv.reader(open("/home/johnson/Desktop/chaloBEST/db_csv_files/AreaMaster.csv", "r"))
    CsvFile.next()
    for entry in CsvFile:
        obj = Area(int(entry[0]), entry[1]) 
        obj.save()
        print obj.a_code, obj.areanm

        print "----- "
    return

def FareLoader():
    CsvFile = csv.reader(open("/home/johnson/Desktop/chaloBEST/chaloBEST/db_csv_files/FareMaster.csv", "r"))
    test = CsvFile.next()
    print test
    for entry in CsvFile:
        obj = Fare(slab=float(entry[0]), ordinary=int(entry[1]), limited=int(entry[2]), express=int(entry[3]), ac=int(entry[4]), ac_express=int(entry[5])) 
        obj.save()
        print obj.__dict__
    return

def RoadLoader():
    CsvFile = csv.reader(open("/home/johnson/Desktop/chaloBEST/db_csv_files/RoadMaster.csv", "r"))
    test = CsvFile.next()
    print test
    for entry in CsvFile:
        obj = Road(roadcd=int(entry[0]), roadnm=str(entry[1])) 
        obj.save()
        print obj.__dict__
    return

def RouteLoader():
    CsvFile = csv.reader(open("/home/johnson/Desktop/chaloBEST/db_csv_files/RouteMaster.csv", "r"), delimiter='\t')
    test = CsvFile.next()
    print test
    for entry in CsvFile:
        obj = Route(route=entry[0], routealias=entry[1], from_stop=entry[2], to_stop=entry[3], distance=float(entry[4]), stages=int(entry[5])) 
        print obj.__dict__
    return

def RouteDetailsLoader():
    CsvFile = csv.reader(open("/home/johnson/Desktop/chaloBEST/db_csv_files/RouteDetails.csv", "r"), delimiter='\t')
    test = CsvFile.next()
    print test
    for entry in CsvFile:
        try:
            print obj.__dict__
            obj = RouteDetails(rno=entry[0], stopsr=int(entry[1]), stopdcd=Stop.objects.get(stopcd=int(entry[2])), stage=entry[3].startswith('1'), km=float(entry[4])) 
            
        except:
            f.write(obj.__dict__)
    return
#RNO,STOPSR,STOPCD,STAGE,KM

def AreaLoader():
    CsvFile = csv.reader(open("/home/johnson/Desktop/chaloBEST/chaloBEST/db_csv_files/RouteDetails.csv", "r"), delimiter='\t')
    f= open('RouteDetailsErrors', 'w')
    test = CsvFile.next()
    print test
    for entry in CsvFile:
        try:    
            obj = RouteDetails(rno=entry[0], stopsr=int(entry[1]), stopcd=Stop.objects.get(stopcd=int(entry[2])), stage=(lambda:entry[3].startswith('1'), lambda:None)[ entry[3] == '' ](), km=(lambda:None,lambda:float(entry[4]))[ entry[4] != '' ]() )
            obj.save()
            obj.__dict__  
        except :
            f.write(str(sys.exc_info()[0]) + str(entry) + '\n') 
            print "Error:", sys.exc_info()[0]

    f.close()

date_format = entry[0].rsplit('.')
theday = int(date_format[0])
themonth = int(date_format[1])
theyear = int('20'+ date_format[2])

import datetime

def holiday_loader():

    CsvFile = csv.reader(open(join(PROJECT_ROOT, "../db_csv_files/Holidays.csv"), "r"), delimiter="\t")
    f= open('HolidaysErrors', 'w')
    test = CsvFile.next()
    print test
    for entry in CsvFile:
        try:    
            date_format = entry[0].rsplit('.')
            theday = int(date_format[0])
            themonth = int(date_format[1])
            theyear = int('20'+ date_format[2])
            obj = Holiday(h_date=datetime.date(day=theday, month=themonth, year=theyear), h_name=str(entry[1])) 
            obj.save()
            obj.__dict__  
        except :
            f.write(str(sys.exc_info()[0]) + str(entry) + '\n') 
            print "Error:", sys.exc_info()[0]

    f.close()
    return

def RouteLoader():
    CsvFile = csv.reader(open(join(PROJECT_ROOT, "../db_csv_files/Route.csv"), "r"), delimiter="\t")
    f= open(join(PROJECT_ROOT, "../db_csv_files/RouteErrors.csv"), 'w')
    header = CsvFile.next()
    print header
    for entry in CsvFile:
        try:    
            obj = Route(route=entry[0], routealias=entry[1], from_stop=entry[2], to_stop=entry[3], distance=float(entry[4]), stages=int(entry[5])) 
            obj.save()
            obj.__dict__ 
        except :
            f.write(str(sys.exc_info()[0]) + str(entry) + '\n') 
            print "Error:", sys.exc_info()[0] + str(entry)

    f.close()
    return 

    obj = Route(route=entry[0], routealias=entry[1], from_stop=entry[2], to_stop=entry[3], distance=float(entry[4]), stages=int(entry[5])) 


def Depot_loader():
    CsvFile = csv.reader(open(join(PROJECT_ROOT, "../db_csv_files/Depot.csv"), "r"), delimiter="\t")
    f= open(join(PROJECT_ROOT, "../db_csv_files/DepotErrors.csv"), 'w')
    header = CsvFile.next()
    print header
    for entry in CsvFile:
        try:    
            obj = Depot(depot_code=str(entry[0]),depot_name=str(entry[1]), stop = Stop.objects.get(stopcd=int(entry[2]))) 
            obj.save()
            obj.__dict__  
        except :
            f.write(str(sys.exc_info()[0]) + str(entry) + '\n') 
            print "Error:", sys.exc_info()[0] + str(entry)

    f.close()
    return



CsvFile = csv.reader(open(join(PROJECT_ROOT, "../db_csv_files/StopMarathi.csv"), "r"), delimiter="\t")
f= open(join(PROJECT_ROOT, "../db_csv_files/StopMarathiErrors.csv"), 'w')
header = CsvFile.next()
print header
for entry in CsvFile:
  try:    
    obj = Stop.objects.get(stopcd=int(entry[0])) 
    obj.stopnm_mr = str(entry[1]) 
    obj.save()
    obj.__dict__  
  except:
    f.write(str(sys.exc_info()[0]) + str(entry) + '\n') 
    print "Error:", sys.exc_info()[0],  str(entry)

f.close()



CsvFile = csv.reader(open(join(PROJECT_ROOT, "../db_csv_files/AreaMarathi.csv"), "r"), delimiter="\t")
f= open(join(PROJECT_ROOT, "../db_csv_files/AreaMarathiErrors.csv"), 'w')
header = CsvFile.next()
print header
for entry in CsvFile:
  try:    
    obj = Area.objects.get(a_code=int(entry[0])) 
    obj.areanm_mr = str(entry[1]) 
    obj.save()
    obj.__dict__  
  except:
    f.write(str(sys.exc_info()[0]) + str(entry) + '\n') 
    print "Error:", sys.exc_info()[0],  str(entry)

f.close()





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

CsvFile = csv.reader(open("/home/johnson/Desktop/chaloBEST/chaloBEST/db_csv_files/Stop.csv", "r"), delimiter='\t')
for entry in CsvFile:
    obj = Stop(stopcd=int(entry[0]), stopnm=str(entry[1]), stopfl=str(entry[2]), chowki=(entry[3]).startswith('TRUE'), roadcd=Road.objects.get(roadcd=int(entry[4])), a_code=Area.objects.get(a_code=int(entry[5])), depot=str(entry[6]) ) 
    obj.save()
    print obj.__dict__


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



"""
AreaCsv = csv.reader(open("/home/johnson/Desktop/chaloBEST/db_csv_files/AreaMaster.csv", "r"))
AreaCsv = csv.reader(open("/home/johnson/Desktop/chaloBEST/db_csv_files/AreaMaster.csv", "r"))
AreaCsv = csv.reader(open("/home/johnson/Desktop/chaloBEST/db_csv_files/AreaMaster.csv", "r"))
AreaCsv = csv.reader(open("/home/johnson/Desktop/chaloBEST/db_csv_files/AreaMaster.csv", "r"))
AreaCsv = csv.reader(open("/home/johnson/Desktop/chaloBEST/db_csv_files/AreaMaster.csv", "r"))
"""
