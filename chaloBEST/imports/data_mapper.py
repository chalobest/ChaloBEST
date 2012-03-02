

saveorder = ["Fare","Holiday","Area","Road","Depot","Stop", "StopMarathi","AreaMarathi","RouteDetail", "Route","RouteType","HardCodedRoute"]

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
    "AreaMarathi":AreaMarathi_save   
}

# There is no model as StopMarathi/AreaMarathi, but this is done to separate errors arising from different input files.

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
    postclean.copydefaultStopLocations()
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
