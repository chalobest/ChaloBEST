from rapidsms.apps.base import AppBase 
import re
import arrest

MAX_MSG_LEN = 160
DIGIT = re.compile(r"\d{1,3}")
PUNCT = re.compile(r"[^\w\s]")
STYLE = {
    "start":   "-* ",
    "repeat": " -*- ",
    "end":     " *-"
}


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
            origin, destination = stops[0]['properties'], stops[-1]['properties']
            msg.respond("%s: %s (%s) to %s (%s)" % (
                    ",".join(routes),
                    origin['display_name'], origin['area'],
                    destination['display_name'], destination['area']))
        else:
            stops = ChaloBest.stops(q=msg.text)['features']
            if not stops:
                msg.respond("Sorry, we found no stops like '%s'." % msg.text)
                return
            response = STYLE["start"]
            for feature in stops:
                stop = feature['properties']
                area = PUNCT.sub('', stop['area'])
                match = "%s (%s): %s" % (stop['official_name'], area, stop['routes'])
                if len(response) > len(STYLE["repeat"]): response += STYLE["repeat"]
                response += match
                if len(response) > MAX_MSG_LEN: break
            if len(response) > MAX_MSG_LEN:
                response = response[:MAX_MSG_LEN-(len(STYLE["end"])+4)] + "..."
            response += STYLE["end"]
            msg.respond(response)
