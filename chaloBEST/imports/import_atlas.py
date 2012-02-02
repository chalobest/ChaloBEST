from settings import PROJECT_ROOT
from os.path import join
import json
import csv
import pdb #debugger
from mumbai.models import *
from fuzzywuzzy import process as fuzzprocess
import datetime

'''
Convert Atlas.csv file (obtained from BEST) into first stage Atlas.json
(step 1)
'''
def csvToJSON():
    atlasCSV = csv.reader(open(join(PROJECT_ROOT, "../db_csv_files/Atlas.csv"), "r"), delimiter="\t")
    atlasDict = {}
    previousRoute = None
    for a in atlasCSV:
        routeNo = a[1].strip()
#        print a
        if routeNo != '':
            atlasDict[routeNo] = [a]
            previousRoute = routeNo
        else:
            atlasDict[previousRoute].append(a) 
#    print atlasDict
    jsonFile = open(join(PROJECT_ROOT, "../db_csv_files/Atlas.json"), "w")
    jsonFile.write(json.dumps(atlasDict, indent=2))
    jsonFile.close()

'''
function to copy over values of AM N PM + Schedule from previous row, reading from Atlas.json, writing to atlasCopied.json
(fill in blank rows where 'copy from previous' is assumed, and create new json file - step 2)
NOTE: this omits routes for which we dont have routeAlias to code mapping for in routeMapping.json
'''
def processJSON():
    routeErrors = {'routes': [], 'others': []}
    routeMapping = json.loads(open(join(PROJECT_ROOT, "../db_csv_files/routeMapping.json")).read())    
    routes = json.loads(open(join(PROJECT_ROOT, "../db_csv_files/Atlas.json")).read())
    previousRow = []
    outDict = {}
    for key in routes.keys():
        print key
        if key not in routeMapping: #make note of routeNames we dont have routeAlias for yet.
            routeErrors['routes'].append(key) 
        else:  #else, go ahead ..
            routeAlias = routeMapping[key]
            thisRoute = routes[key]
            #handle copying over empty values from previous rows
            outDict[key] = []
            for row in thisRoute:
               # pdb.set_trace()
                if len(row) < 7:
                    routeErrors['others'].append({key: row})  
                    break  
                for i in range(2,4):
                    if row[i].strip() == '':
                        row[i] = previousRow[i]
                try:
                    if row[-5].strip() == '':
                        row[-5] = previousRow[-5]
                except:
                    pdb.set_trace()
                previousRow = row
                outDict[key].append(row)

    atlasRouteErrors = open("atlasRouteErrors.json", "w")
    atlasRouteErrors.write(json.dumps(routeErrors, indent=2))
    atlasRouteErrors.close()
    atlasCopied = open(join(PROJECT_ROOT, "../db_csv_files/atlasCopied.json"), "w")
    atlasCopied.write(json.dumps(outDict, indent=2))
    atlasCopied.close()

'''
function to group atlasCopied.json to uniqueRoutes (uniqueRoutes.json)
(step 3)
'''
def groupUnique():
    routes = json.loads(open(join(PROJECT_ROOT, "../db_csv_files/atlasCopied.json")).read())
    errors = {}
    outDict = {}
    for key in routes.keys():

        
        outDict[key] = []
        for row in routes[key]:
            print key
            d = {
                'from': row[7],
                'to': row[10],                
                'span': row[13],
                'is_full': False,
#                'schedule': row[28],
#                'rows': {
#                    row[-5]: row
#                }   
            }
            matchedRow = isNotUnique(d, outDict[key])
            schedule = row[-5]
            if matchedRow is not None:
                outDict[key][matchedRow]['rows'][schedule] = row
            else:
                if isLargestSpan(d, routes[key]):
                    d['is_full'] = True
                outDict[key].append(d)
                if not outDict[key][-1].has_key('rows'):
                    outDict[key][-1]['rows'] = {}
                outDict[key][-1]['rows'][schedule] = row

    outFile = open(join(PROJECT_ROOT, "../db_csv_files/uniqueRoutes.json"), "w")
    outFile.write(json.dumps(outDict, indent=2))
    outFile.close()


'''
Go through uniqueRoutes.json and actually import atlas data into the db
(step 4)
'''
def importUniqueRoutes():
    data = json.load(open(join(PROJECT_ROOT, "../db_csv_files/uniqueRoutes.json")))
    routeMapping = json.load(open(join(PROJECT_ROOT, "../db_csv_files/routeMapping.json")))
    routeDoesNotExistErrors = [] #route codes for which there are entries in routeMapping.json and in Atlas, but which do not exist in RouteMaster
    stopMapping = {} #FIXME
    stopErrors = [] #This should ideally never happen, and any errors here are bad and would indicate problems with the fuzzy matching logic, most likely.
    for route in data.keys():
        if routeMapping.has_key(route):
            routeCode = routeMapping[route]
            try:
                routeObj = Route.objects.get(code=routeCode)
            except:
                routeDoesNotExistErrors.append({'routeCode': routeCode, 'routeAlias': route})
                continue
        else:
            try:
                routeObj = Route.objects.get(alias=route)
            except:
                routeDoesNotExistErrors.append({'routeAlias': route})

        for unique_route in data[route]:
            thisRoute = unique_route #FIXME
            try:
                distance = float(thisRoute['span'])
            except:
                distance = 0
            obj = UniqueRoute(route=routeObj, is_full=thisRoute['is_full'], distance=distance, from_stop_txt=thisRoute['from'], to_stop_txt=thisRoute['to']) 
            if obj.is_full: #If the route is the primary route, we can get stop codes easily from RouteDetails first / last stop
                from_to = getFromToStopsForRoute(routeObj.code)
                obj.from_stop = from_to[0]
                if not stopMapping.has_key(obj.from_stop_txt):
                    stopMapping[obj.from_stop_txt] = from_to[0].stop
                obj.to_stop = from_to[1]
                if not stopMapping.has_key(obj.to_stop_txt):
                    stopMapping[obj.to_stop_txt] = from_to[1].stop
            else: #Else we do fuzzy string matching against all possible values for stopname got from RouteDetails
                stopnames = []
                stopcodes = []
                for r in RouteDetails.objects.filter(route=routeObj):
                    stopnames.append(r.stop.name)
                    stopcodes.append(r.stop.code)     
                from_fuzz = fuzzprocess.extractOne(thisRoute['from'], stopnames)
                to_fuzz = fuzzprocess.extractOne(thisRoute['to'], stopnames)
                #pdb.set_trace()
                try:
                    obj.from_stop = Stop.objects.filter(name=from_fuzz[0]).filter(code__in=stopcodes)[0]
                    obj.to_stop = Stop.objects.filter(name=to_fuzz[0]).filter(code__in=stopcodes)[0]
                except:
                    stopErrors.append([thisRoute['from'], thisRoute['to']])
                    continue
                
            obj.save()
            #pdb.set_trace()
#            print thisRoute['rows'].keys()
            for schedule in thisRoute['rows'].keys(): #loop through each schedule per UniqueRoute and save it
                row = thisRoute['rows'][schedule]
                try:
                    depot = Depot.objects.get(code=row[6])
                except:
                    depot = None #FIXME!! Catch depot errors based on findings
                #pdb.set_trace()
                routeScheduleObj = RouteSchedule(unique_route=obj, schedule_type=schedule, busesAM=noneInt(row[2]), busesN=noneInt(row[3]), busesPM=noneInt(row[4]), bus_type=row[5], depot_txt=row[6], depot=depot, first_from=formatTime(row[8]), last_from=formatTime(row[9]), first_to=formatTime(row[11]), last_to=formatTime(row[12]), runtime1=noneInt(row[14]), runtime2=noneInt(row[15]), runtime3=noneInt(row[16]), runtime4=noneInt(row[17]), headway1=noneInt(row[18]), headway2=noneInt(row[19]), headway3=noneInt(row[20]), headway4=noneInt(row[21]), headway5=noneInt(row[22]))
                routeScheduleObj.save()

    #done saving things - write out error files:
    errors = open(join(PROJECT_ROOT, "../errors/routeMasterMissingRoutes.json"), "w")
    errors.write(json.dumps(routeDoesNotExistErrors, indent=2))
    errors.close()
    stopMappingFile = open(join(PROJECT_ROOT, "../db_csv_files/stopMapping.json"), "w")
    stopMappingFile.write(json.dumps(stopMapping, indent=2))                        
    stopMappingFile.close()
    stopErrorsFile = open(join(PROJECT_ROOT, "../errors/atlasStopErrors.json"), "w")
    stopErrorsFile.write(json.dumps(stopErrors, indent=2))
    stopErrorsFile.close()

'''
>>>formatTime("06.40")
>>>time(6,40)
'''
def formatTime(s):
    if s.strip() == '':
        return datetime.time(0,0)
    split = s.split(".")
    try:
        hour = int(split[0])
    except:
        hour = 0
    try:
        minutes = int(split[1])
    except:
        minutes = 0 #FIXME: ugly!!
    #pdb.set_trace()
    try:
        return datetime.time(hour, minutes)
    except:
        return datetime.time(0,0)

'''
Silly function to deal wth invalid strings in the data that need to go in as Integers into the db
passed a string, it will either return int(string) or None if that fails for any reason
FIXME: find a more elegant way to do this
'''
def noneInt(val):
    try:
        return int(val)
    except:
        return None

'''
Passed a route code, it gets stop codes for the first and last stop
'''
def getFromToStopsForRoute(routeCode):
#    fromStr = row[2]
    routeDetails = RouteDetails.objects.filter(rno=routeCode).order_by('stopsr')
    if routeDetails.count() == 0:
        return None
    fromStop = routeDetails[0].stop
    toStop = routeDetails[routeDetails.count() -1].stop
    return (fromStop, toStop,)
    
    
'''
checks whether the row in a set of rows for a route has the largest 'span' value, useful to tell if a row belongs to a primary route
params:
  data - dict with a span attribute
  arr - array of rows to check if data['span'] is greater than. span is at row[13]
'''
def isLargestSpan(data, arr):
    span = data['span']
    for a in arr:
        try:
            arrSpan = float(a[13])
        except:
            arrSpan = 0
        try:
            dataSpan = float(data['span'])
        except:
            dataSpan = 0
        if arrSpan > dataSpan:
            return False
    return True

'''
    returns index of row if not unique, else None
'''
def isNotUnique(data, arr):
    i = 0
    for a in arr:
        if a['from'] == data['from'] and a['to'] == data['to']:
            return i
        i += 1
    return None

'''
Create routeMapping.json file to map route aliases to route codes
TODO: add mappings from hard coded routes
'''
def getRouteCodes():
    atlasRawCSV = csv.reader(open(join(PROJECT_ROOT, "../db_csv_files/AtlasRaw.csv"), "r"), delimiter="\t")
    atlasDict = json.loads(open(join(PROJECT_ROOT, "../db_csv_files/Atlas.json")).read())
    mapping = {}
    missingFile = open("/tmp/routesMissing.txt", "w")
    for row in atlasRawCSV:
        routeAlias = row[0]
        routeCode = row[1]
        print routeCode
        if routeCode in atlasDict:
            mapping[routeCode] = routeAlias
        else:
            missingFile.write(routeCode + "\n")
    missingFile.close()
    mappingFile = open(join(PROJECT_ROOT, "../db_csv_files/routeMapping.json"), "w")
    mappingFile.write(json.dumps(mapping, indent=2))
    mappingFile.close()


'''
Import RouteMaster into db
'''
def importRouteMaster():
    CsvFile = csv.reader(open(join(PROJECT_ROOT, "../db_csv_files/RouteMaster.csv"), "r"), delimiter=',')
    test = CsvFile.next()
    stop_errors = []
    print test
    for row in CsvFile:
        if len(row) < 1:
            continue
        from_to = getFromToStopsForRoute(row[0])
        if from_to is None:
            stop_errors.append(row[0])
            continue
        print row[0]
        obj = Route(code=row[0], alias=row[1], from_stop_txt=row[2], to_stop_txt=row[3], from_stop=from_to[0], to_stop=from_to[1], distance=row[4], stages=int(row[5]))
        obj.save()
    errors = open(join(PROJECT_ROOT, "../errors/routeStopErrors.json"), "w")
    errors.write(json.dumps(stop_errors, indent=2))
    errors.close()


def csvClean1():
    atlasCSV = csv.reader(open(join(PROJECT_ROOT, "../db_csv_files/Atlas.csv"), "r"), delimiter="\t")
