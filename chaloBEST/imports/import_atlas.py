from settings import PROJECT_ROOT
from os.path import join
import json
import csv

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
<<<<<<< TREE


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
            
=======
<<<<<<< TREE

def csvClean1():
    atlasCSV = csv.reader(open(join(PROJECT_ROOT, "../db_csv_files/Atlas.csv"), "r"), delimiter="\t")
	
=======


>>>>>>> MERGE-SOURCE
>>>>>>> MERGE-SOURCE
