from settings import PROJECT_ROOT
from os.path import join
import json
import csv
import pdb

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
            
