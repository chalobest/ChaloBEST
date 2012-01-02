from settings import PROJECT_ROOT
from os.path import join
import json
import csv

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




def csvClean1():
    atlasCSV = csv.reader(open(join(PROJECT_ROOT, "../db_csv_files/Atlas.csv"), "r"), delimiter="\t")
