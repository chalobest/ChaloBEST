from rapidsms.apps.base import AppBase 
import re
import arrest
import operator
import re
import string
try:
   import json
except ImportError:
   import simplejson as json
import ast


MAX_MSG_LEN = 160
DIGIT = re.compile(r"\d{1,3}")
PUNCT = re.compile(r"[^\w\s]")
"""
STYLE = {
    "start":   "-* ",
    "repeat": " -*- ",
    "end":     " *-"
}
"""

STYLE = {"start": "", "repeat": "; ", "end": ""}


#ChaloBest = arrest.Client("http://chalobest.in/1.0")
ChaloBest = arrest.Client("http://dev.chalobest.in/1.0")

def get_routes_for_matches(stops):
#    same_stops = []
#    same_stops.append(stops[0])
#    if len(stops) > 1:
#        for s in stops[1:]:
#            if s['properties']['official_name'] == stops[0]['properties']['official_name']:
#                same_stops.append(s)
    routes = []
    for stop in stops:
        routes.extend(stop['properties']['routes'].split(", "))
    return routes            

def get_stops_for_string(s):
    '''
        Returns a dict with name and stops to associate with given search string.
        First looks at areas, if string matches an area, returns area as name and all stops within that area as stops.
        If search term does not match an area, returns the first / best match of stop to string. If there are multiple stops with the same name, returns all of them in the list of stops.
    '''
    stops = []
    s = s.strip()
#    areas = ChaloBest.areas(q=s)
    areas = [area for area in ChaloBest.areas(q=s) if area.lower().startswith(s)]
    if len(areas) > 0:
        for a in areas:
            area = ChaloBest.area[a]
            for stop in area['stops']['features']:        
                stops.append(stop)
        return {
            'name': ", ".join(areas),
            'stops': stops
        }
    else:
        stops_results = ChaloBest.stops(q=s)['features']
        if len(stops_results) == 0:
            return None
        same_stops = []
        same_stops.append(stops_results[0])
        if len(stops_results) > 1:
            for s in stops_results[1:]:
                if s['properties']['official_name'] == same_stops[0]['properties']['official_name']:
                    same_stops.append(s)               
        return {
            'name': same_stops[0]['properties']['display_name'],
            'stops': same_stops
        }

class App(AppBase):
    def handle(self, msg):
        if DIGIT.search(msg.text):
            routes = ChaloBest.routes(q=msg.text.replace(" ", ""))
            pattern = str(str(msg.text).translate(None, string.digits))
	    import collections
            result = collections.defaultdict(list)
            #print routeO
            for d in routes:
                result[d['code']].append(d)
            someList = result.values()
            #print len(someList)
            #print someList
            #pattern = "A".upper()
	    detail =[]
	    my_default = someList[0]
	    someList.sort(key=operator.itemgetter(0))
            for item in someList:
                    #print item[0].__class__
                    #try:
                    #       tt=ast.literal_eval(json.dumps(item[0]))
                    #except ValueError:
                    #       tt=ast.literal_eval(json.dumps(item[0]))
                    for key, value in item[0].items():
                            if key == "route_type_aliases":
				
                                if len(value.strip())==0 and len(pattern.strip())==0:
                                    detail.append(str(item[0].get("display_name")))
				    detail.append(str(item[0].get("start_stop")))
				    detail.append(str(item[0].get("start_area")))
				    detail.append(str(item[0].get("end_stop")))
				    detail.append(str(item[0].get("end_area")))
				    detail.append(str(item[0].get("headway")))
				    detail.append(str(item[0].get("url")))
				    detail.append(str(item[0].get("distance")))
				    
				   # return busname
                                if len(pattern.strip())!=0 and pattern.strip().upper() in value.upper():
				    detail.append(str(item[0].get("display_name")))
                                    detail.append(str(item[0].get("start_stop")))
                                    detail.append(str(item[0].get("start_area")))
                                    detail.append(str(item[0].get("end_stop")))
                                    detail.append(str(item[0].get("end_area")))
                                    detail.append(str(item[0].get("headway")))
                                    detail.append(str(item[0].get("url")))
                                    detail.append(str(item[0].get("distance")))
				if len(pattern.strip())==0 and value.strip() is not None:
				    detail.append(str(item[0].get("display_name")))
				    detail.append(str(item[0].get("start_stop")))
				    detail.append(str(item[0].get("start_area")))
				    detail.append(str(item[0].get("end_stop")))
				    detail.append(str(item[0].get("end_area")))
				    detail.append(str(item[0].get("headway")))
				    detail.append(str(item[0].get("url")))
				    detail.append(str(item[0].get("distance")))
									


	
				    #return busname

            if not routes:
                msg.respond("Sorry, we found no route marked '%(text)s'.", text=msg.text)
                return
            url = "http://dev.chalobest.in" + str(detail[6])
	    distance = str(detail[7])+" kms"
            if str(detail[5]).strip() is not None:
                headway = "Freq: " + str(detail[5]) + " mins"
            else:
                headway = "No bus now."
            response = "%s: %s (%s) to %s (%s). %s. %s %s" % (str(detail[0]), str(detail[1]), str(detail[2]), str(detail[3]), str(detail[4]),str(headway), str(url), str(distance))

        elif msg.text.find(" to ") != -1:

            from_txt = msg.text.lower().split("to")[0].strip()
            to_txt = msg.text.lower().split("to")[1].strip()

            from_matches = get_stops_for_string(from_txt)
            to_matches = get_stops_for_string(to_txt)

#            stop1matches = ChaloBest.stops(q=stop1txt)['features']
            if not from_matches:
                msg.respond("Sorry, found no stop matching '%s'" % from_txt)
                return
            #best_match1 = stop1matches[0]
            routes1 = set(get_routes_for_matches(from_matches['stops']))
            #stop2matches = ChaloBest.stops(q=stop2txt)['features']
            if not to_matches:
                msg.respond("Sorry, found no stop matching '%s'" % to_txt)
            #best_match2 = stop2matches[0]
            routes2 = set(get_routes_for_matches(to_matches['stops']))
            #routes1arr = set(routes1.split(", "))
            #routes2arr = set(routes2.split(", "))
            intersection = list(routes1.intersection(routes2))
            if len(intersection) == 0:
                msg.respond("Sorry, no direct buses found between %s and %s" % (from_matches['name'], to_matches['name'],))
                return
            routesFound = ", ".join(intersection)
            response = "%s to %s: %s" % (from_matches['name'], to_matches['name'], routesFound,)
            if len(response) > MAX_MSG_LEN:
                response = response[0:MAX_MSG_LEN]
            #msg.respond("%s to %s: %s" % (from_matches['name'], to_matches['name'], routesFound,))
            
            

        else:
            features = ChaloBest.stops(q=msg.text)['features']
            if not features:
                msg.respond("Sorry, we found no stops marked '%(text)s'.", text=msg.text)
                return
            stops = []
            for feat in features:
                stop = feat['properties']
                if stops and stop["official_name"] == stops[-1]["official_name"]:
                    stops[-1]["routes"] += ", " + stop["routes"]
                else:
                    stops.append(stop)
            response = STYLE["start"]
            for stop in stops:
                match = stop["display_name"] + ": " + stop["routes"]
                if len(response) > len(STYLE["repeat"]): response += STYLE["repeat"]
                response += match
                if len(response) > MAX_MSG_LEN: break
            if len(response) > MAX_MSG_LEN:
                response = response[:MAX_MSG_LEN-(len(STYLE["end"])+4)] + "..."
            response += STYLE["end"]

        msg.respond(response)

