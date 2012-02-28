from rapidsms.apps.base import AppBase 
import re
import arrest

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


ChaloBest = arrest.Client("http://chalobest.in/1.0")

class App(AppBase):
    def handle(self, msg):
        if DIGIT.search(msg.text):
            routes = ChaloBest.routes(q=msg.text.replace(" ", ""))
            detail = ChaloBest.route[routes[0]]
            stops = detail['stops']['features']
            if not stops:
                msg.respond("Sorry, we found no route marked '%s'." % msg.text)
                return
            origin, dest = stops[0]['properties'], stops[-1]['properties']
            origin_name, dest_name = origin['display_name'], dest['display_name']
            origin_area, dest_area = PUNCT.sub('', origin['area']), PUNCT.sub('', dest['area'])
            msg.respond("%s: %s (%s) to %s (%s)" % (
                    ",".join(routes), origin_name, origin_area, dest_name, dest_area))
        else:
            features = ChaloBest.stops(q=msg.text)['features']
            if not features:
                msg.respond("Sorry, we found no stops like '%s'." % msg.text)
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
                match = stop["official_name"] + ": " + stop["routes"]
                if len(response) > len(STYLE["repeat"]): response += STYLE["repeat"]
                response += match
                if len(response) > MAX_MSG_LEN: break
            if len(response) > MAX_MSG_LEN:
                response = response[:MAX_MSG_LEN-(len(STYLE["end"])+4)] + "..."
            response += STYLE["end"]
            msg.respond(response)
