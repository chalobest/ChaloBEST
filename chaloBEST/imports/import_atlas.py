from settings import PROJECT_ROOT
from os.path import join
import json
import csv
import pdb
from mumbai.models import *
from fuzzywuzzy import process as fuzzprocess
import datetime

#Get levenshtein distance between two strings, from http://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance
def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if not s1:
        return len(s2)
 
    previous_row = xrange(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

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
                'rows': {
                    row[-5]: row
                }   
            }
            matchedRow = isNotUnique(d, outDict[key])
            if matchedRow:
                schedule = row[-5]
                outDict[key][matchedRow]['rows'][schedule] = row
            else:
                if isLargestSpan(d, routes[key]):
                    d['is_full'] = True
                outDict[key].append(d)
    outFile = open(join(PROJECT_ROOT, "../db_csv_files/uniqueRoutes.json"), "w")
    outFile.write(json.dumps(outDict, indent=2))
    outFile.close()


'''
Import RouteMaster
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


def importUniqueRoutes():
    data = json.load(open(join(PROJECT_ROOT, "../db_csv_files/uniqueRoutes.json")))
    routeMapping = json.load(open(join(PROJECT_ROOT, "../db_csv_files/routeMapping.json")))
    routeDoesNotExistErrors = []
    stopMapping = {}
    stopErrors = []
    for route in data.keys():
        routeCode = routeMapping[route]
        try:
            routeObj = Route.objects.get(code=routeCode)
        except:
            routeDoesNotExistErrors.append({'routeCode': routeCode, 'routeAlias': route})
            continue
        for unique_route in data[route]:
            thisRoute = unique_route #FIXME
            try:
                distance = float(thisRoute['span'])
            except:
                distance = 0
            obj = UniqueRoute(route=routeObj, is_full=thisRoute['is_full'], distance=distance, from_stop_txt=thisRoute['from'], to_stop_txt=thisRoute['to'])
            if obj.is_full:
                from_to = getFromToStopsForRoute(routeObj.code)
                obj.from_stop = from_to[0]
                if not stopMapping.has_key(obj.from_stop_txt):
                    stopMapping[obj.from_stop_txt] = from_to[0].stopcd
                obj.to_stop = from_to[1]
                if not stopMapping.has_key(obj.to_stop_txt):
                    stopMapping[obj.to_stop_txt] = from_to[1].stopcd
            else:
                stopnames = []
                stopcodes = []
                for r in RouteDetails.objects.filter(rno=routeObj.code):
                    stopnames.append(r.stopcd.stopnm)
                    stopcodes.append(r.stopcd.stopcd)     
                from_fuzz = fuzzprocess.extractOne(thisRoute['from'], stopnames)
                to_fuzz = fuzzprocess.extractOne(thisRoute['to'], stopnames)
                #pdb.set_trace()
                try:
                    obj.from_stop = Stop.objects.filter(stopnm=from_fuzz[0]).filter(stopcd__in=stopcodes)[0]
                    obj.to_stop = Stop.objects.filter(stopnm=to_fuzz[0]).filter(stopcd__in=stopcodes)[0]
                except:
                    stopErrors.append([thisRoute['from'], thisRoute['to']])
                    continue
            obj.save()
            #pdb.set_trace()
#            print thisRoute['rows'].keys()
            for schedule in thisRoute['rows'].keys(): 
                row = thisRoute['rows'][schedule]
                try:
                    depot = Depot.objects.get(depot_code=row[6])
                except:
                    depot = None
                #pdb.set_trace()
                routeScheduleObj = RouteSchedule(unique_route=obj, schedule_type=schedule, busesAM=noneInt(row[2]), busesN=noneInt(row[3]), busesPM=noneInt(row[4]), bus_type=row[5], depot_txt=row[6], depot=depot, first_from=formatTime(row[8]), last_from=formatTime(row[9]), first_to=formatTime(row[11]), last_to=formatTime(row[12]), runtime1=noneInt(row[14]), runtime2=noneInt(row[15]), runtime3=noneInt(row[16]), runtime4=noneInt(row[17]), headway1=noneInt(row[18]), headway2=noneInt(row[19]), headway3=noneInt(row[20]), headway4=noneInt(row[21]), headway5=noneInt(row[22]))
                routeScheduleObj.save()
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

def noneInt(val):
    try:
        return int(val)
    except:
        return None

def getFromToStopsForRoute(routeCode):
#    fromStr = row[2]
    routeDetails = RouteDetails.objects.filter(rno=routeCode).order_by('stopsr')
    if routeDetails.count() == 0:
        return None
    fromStop = routeDetails[0].stopcd
    toStop = routeDetails[routeDetails.count() -1].stopcd
    return (fromStop, toStop,)
    
    

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
    returns index of row if not unique, else False
'''
def isNotUnique(data, arr):
    i = 0
    for a in arr:
        if a['from'] == data['from'] and a['to'] == data['to'] and a['span'] == data['span']:
            return i
        i += 1
    return False


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



def csvClean1():
    atlasCSV = csv.reader(open(join(PROJECT_ROOT, "../db_csv_files/Atlas.csv"), "r"), delimiter="\t")
