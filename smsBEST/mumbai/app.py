from rapidsms.apps.base import AppBase 
import re
import arrest

DIGIT = re.compile(r"\d{1,3}")
chalobest = arrest.Client("http://chalobest.in/1.0")

class App(AppBase):
    def handle(self, msg):
        if DIGIT.search(msg.text):
            routes = chalobest.routes(q=msg.text.replace(" ", ""))
            detail = chalobest.route[routes[0]]
            stops = detail['stops']['features']
            origin, destination = stops[0]['properties'], stops[-1]['properties']
            msg.respond("%s: %s (%s) to %s (%s)" % (routes[0],
                    origin['display_name'], origin['area'],
                    destination['display_name'], destination['area']))
        else:
            stops = chalobest.stops(q=msg.text)
            stop = stops['features'][0]['properties']
            msg.respond("%s (%s): %s" % (stop['official_name'], stop['area'], stop['routes']))
