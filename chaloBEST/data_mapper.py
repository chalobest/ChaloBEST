from mumbai.models import *
import csv

CsvFile = csv.reader(open("/home/johnson/Desktop/chaloBEST/db_csv_files/AreaMaster.csv", "r"))
CsvFile.next()
for entry in CsvFile:
    obj = Area(int(entry[0]), entry[1]) 
    obj.save()
    print obj.a_code, obj.areanm

print "----- "

CsvFile = csv.reader(open("/home/johnson/Desktop/chaloBEST/db_csv_files/FareMaster.csv", "r"))
test = CsvFile.next()
print test
for entry in CsvFile:
    obj = Fare(slab=float(entry[0]), ordinary=int(entry[1]), limited=int(entry[2]), express=int(entry[3]), ac=int(entry[4]), ac_express=int(entry[5])) 
    obj.save()
    print obj.__dict__


CsvFile = csv.reader(open("/home/johnson/Desktop/chaloBEST/db_csv_files/RoadMaster.csv", "r"))
test = CsvFile.next()
print test
for entry in CsvFile:
    obj = Road(roadcd=int(entry[0]), roadnm=str(entry[1])) 
    obj.save()
    print obj.__dict__


CsvFile = csv.reader(open("/home/johnson/Desktop/chaloBEST/db_csv_files/RouteMaster.csv", "r"), delimiter='\t')
test = CsvFile.next()
print test
for entry in CsvFile:
    obj = Route(route=entry[0], routealias=entry[1], from_stop=entry[2], to_stop=entry[3], distance=float(entry[4]), stages=int(entry[5])) 
    print obj.__dict__


CsvFile = csv.reader(open("/home/johnson/Desktop/chaloBEST/db_csv_files/RouteDetails.csv", "r"))
test = CsvFile.next()
print test
for entry in CsvFile:
    obj = RouteDetails(rno=entry[0], stopsr=int(entry[1]), stopcd=int(entry[2]), stage=entry[3].startswith('TRUE'), km=float(entry[4])) 
    print obj.__dict__




CsvFile = csv.reader(open("/home/johnson/Desktop/chaloBEST/db_csv_files/Stop.csv", "r"), delimiter='\t')
test = CsvFile.next()
print test
for entry in CsvFile:
    obj = Stop(stopcd=int(entry[0]), stopnm=str(entry[1]), stopfl=str(entry[2]), chowki=(entry[3]).startswith('TRUE'), roadcd=Road.objects.get(roadcd=int(entry[4])), a_code=Area.objects.get(a_code=int(entry[5])), depot=str(entry[6]) ) 
    obj.save()
    print obj.__dict__


CsvFile = csv.reader(open("/home/johnson/Desktop/chaloBEST/db_csv_files/AreaMaster.csv", "r"))
CsvFile.next()
for entry in CsvFile:
    obj = AreaMaster(int(entry[0]), entry[1]) 
    obj.save()










"""
AreaCsv = csv.reader(open("/home/johnson/Desktop/chaloBEST/db_csv_files/AreaMaster.csv", "r"))
AreaCsv = csv.reader(open("/home/johnson/Desktop/chaloBEST/db_csv_files/AreaMaster.csv", "r"))
AreaCsv = csv.reader(open("/home/johnson/Desktop/chaloBEST/db_csv_files/AreaMaster.csv", "r"))
AreaCsv = csv.reader(open("/home/johnson/Desktop/chaloBEST/db_csv_files/AreaMaster.csv", "r"))
AreaCsv = csv.reader(open("/home/johnson/Desktop/chaloBEST/db_csv_files/AreaMaster.csv", "r"))
"""
