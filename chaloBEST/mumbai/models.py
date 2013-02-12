from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import connection
import json
from django.contrib.gis.measure import D
import datetime
from gtfs.gtfs_export import time_of

STOP_CHOICES = ( ('U','Up'),
                 ('D', 'Down'),
                 )

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

SCHED = {
    'MS':[1, 2, 3, 4, 5, 6],
    'HOL':[7, 8],
    'SUN':[7],
    'MF&HOL':[1, 2, 3, 4, 5, 8],
    'SAT':[6],
    'MF':[1, 2, 3, 4, 5],
    'SH':[7, 8],
    'AD':[1, 2, 3, 4, 5, 6, 7, 8],
    'SAT&SUN':[6, 7],
    'MS&HOL':[1, 2, 3, 4, 5, 6, 8],
    'FW':[1, 2, 3, 4, 5, 6, 7],
    'MS&SUN':[1, 2, 3, 4, 5, 6, 7],
    'SAT/SH':[6, 7, 8],
    'SAT&HOL':[6, 8],
    'SAT&SH':[6, 7, 8],
    'SAT/SUND&HOL':[6, 7, 8],
    'S/H':[7, 8],
    'SAT,SUN&HOL':[6, 7, 8],
    'FH':[5, 8]
    }






# Runtime start and end hour
# matching column `runtime$` where `$` = index % 4 + 1
RUNTIMES = (
    (00, 07), 
    (07, 11),
    (11, 17),
    (17, 20),
    (20, 24)
)

class TrigramSearchManager(models.GeoManager):
    def __init__(self, trigram_columns=[]):
        super(TrigramSearchManager, self).__init__()
        self.trigram_columns = trigram_columns

    def set_threshold(self, threshold):
        """Set the limit for trigram similarity matching."""
        cursor = connection.cursor()
        cursor.execute("""SELECT set_limit(%f)""" % threshold)

    def find_approximate(self, text, match=0.5):
        self.set_threshold(match)
        similarity_measure = "greatest(%s)" % ",".join(["similarity(%s, %%s)" % col for col in self.trigram_columns])
        similarity_filter = " OR ".join(["%s %%%% %%s" % col for col in self.trigram_columns])
        text_values = [text] * len(self.trigram_columns)
        qset = self.get_query_set()
        # use the pg_trgm index via the % operator
        qset = qset.extra(select={"similarity":similarity_measure},
                          select_params=text_values,
                          where=[similarity_filter],
                          params=text_values,
                          order_by=["-similarity"])
        return qset

class Area(models.Model):
    objects = TrigramSearchManager(("name", "name_mr", "display_name"))
    code = models.IntegerField() #primary_key=True)
    slug = models.SlugField(null=True)
    name = models.TextField(blank=True, max_length=255)
    name_mr= models.TextField(null=True, blank=True, max_length=512) #null=True, 
    display_name = models.TextField(blank=True, max_length=255)
    geometry = models.PolygonField(blank=True, null=True)
    alt_names = generic.GenericRelation("AlternativeName")

    def get_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'slug': self.slug,
            'name': self.name,
            'name_mr': self.name_mr,
            'display_name': self.display_name,
            'url': self.get_absolute_url()
            #FIXME add alt_names and geometry
        }

    
    def get_autocomplete(self):
        '''
        Returns a dict to be used by the autocomplete front-end
        '''
        return {
            'id': self.id,
            'type': 'Area',
            'title': self.display_name,
            'url': self.get_absolute_url()
        }

    def get_absolute_url(self):
        return "/area/%s/" % self.slug

    def __unicode__(self):
        return self.name   

    #FIXME: ideally this would be done using the polygon of the area, but right now we take a random stop in the area, find all stops within x kms, and then return unique areas for those stops.    
    @property
    def nearby_areas(self, distance=D(km=3)):
        stop = self.stop_set.all()[0]
        tup = (stop.point, distance,)
        qset = Stop.objects.filter(point__distance_lte=tup).values('area').distinct()
        area_ids = [val['area'] for val in qset]
        return Area.objects.filter(pk__in=area_ids)    

    @property
    def routes_passing(self):
        return Route.objects.filter(routedetail__stop__area=self).distinct()
        

class Road(models.Model):
    code = models.IntegerField()#primary_key=True)
    slug = models.SlugField(null=True)
    name = models.TextField(blank=True, max_length=255)
    name_mr= models.TextField(null=True, blank=True, max_length=512)
    display_name = models.TextField(blank=True, max_length=255)
    geometry = models.LineStringField(blank=True, null=True)
    alt_names = generic.GenericRelation("AlternativeName")

    def __unicode__(self):
        return self.name   


class Fare(models.Model):
    slab = models.DecimalField(max_digits=5, decimal_places=2) 
    ordinary = models.PositiveIntegerField()
    limited = models.PositiveIntegerField()
    express = models.PositiveIntegerField()
    ac = models.PositiveIntegerField()
    ac_express = models.PositiveIntegerField()
    def __unicode__(self):
        return str(self.slab)   

class Stop(models.Model):
    objects = TrigramSearchManager(("name", "name_mr", "display_name"))
    code = models.IntegerField(db_index=True)
    slug = models.SlugField(null=True)
    name = models.TextField(blank=True, max_length=255, db_index=True)
    display_name = models.TextField(blank=True, max_length=255)
    dbdirection = models.CharField(null=True, blank=True, max_length=5, choices=STOP_CHOICES) #stopfl - > direction
    chowki = models.NullBooleanField(null=True, blank=True) # this is nullable since in the next datafeed , they might have blank to represent a 0.
    road = models.ForeignKey(Road, default=None, null=True, blank=True)
    area = models.ForeignKey(Area, default=None, null=True, blank=True)
    depot = models.ForeignKey("Depot", default=None, null=True, blank=True, related_name="is_depot_for") #models.CharField(null=True, blank=True, max_length=5)
    name_mr= models.TextField(null=True, blank=True, max_length=512)#null=True
    point = models.PointField(null=True)
    alt_names = generic.GenericRelation("AlternativeName")

    def get_autocomplete(self):
        '''
        Returns a dict to be used by the autocomplete front-end
        '''
        return {
            'id': self.id,
            'type': 'Stop',
            'title': "%s (%s)" % (self.display_name, self.area.display_name,),
            'url': self.get_absolute_url()
        }

    def get_routes(self):
        routes = []
        for r in self.routedetail_set.all():
            if r.route is not None:
                routes.append(r.route)
        return routes        

    def get_dict(self):
        #routes = self.get_routes()
        return {
            'id': self.id,
            'code': self.code,
            'slug': self.slug,
            'official_name': self.name,
            'display_name': self.display_name,
            'road': self.road.display_name,
            'road_mr': self.road.name_mr,
            'area': self.area.display_name,
            'area_mr': self.area.name_mr,
            'area_url': self.area.get_absolute_url(),
            'name_mr': self.name_mr,
            'direction': self.dbdirection,
            'routes': ", ".join([r.display_name for r in self.routes]),
            'alternative_names': ", ".join([a.name for a in self.alt_names.all()]),
            'url': self.get_absolute_url()
        }

    def get_geojson(self, srid=4326):
#        print srid
        if self.point is not None:
            geom = json.loads(self.point.transform(srid, True).geojson)
        else:
            geom = {}

        properties = self.get_dict()

        return {
            'type': 'Feature',
            'properties': properties,
            'geometry': geom
        }        

    def from_geojson(self, geojson, srid=4326):
        geom = geojson['geometry']['coordinates']
        data = geojson['properties']
        point = Point(geom[0], geom[1], srid=srid).transform(4326, True)
        if point:
            self.point = point
        self.display_name = data['display_name']
        self.name_mr = data['name_mr']
        if data.has_key('alternative_names') and data['alternative_names'].strip() != '':
            for a in self.alt_names.all():
                a.delete()
            for a in data['alternative_names'].split(","):
                alt_name = AlternativeName()
                alt_name.name = a.strip()
                alt_name.typ = 'common'
                alt_name.content_object = self
                alt_name.save()
                self.alt_names.add(alt_name)    
        self.save()
        return self.get_geojson(srid=srid)

    @property
    def nearby_stops(self, dist=D(km=0.5)):
        tup = (self.point, dist,)
        return Stop.objects.filter(point__distance_lte=tup)

    @property
    def routes(self):
        return Route.objects.filter(routedetail__stop=self)

    @property    
    def display_alt_names(self):
        '''
            Exclude the display_name from the alt name results and return alt names
        '''
        alt_names = []
        for a in self.alt_names.all():
            if a.name != self.display_name:
                alt_names.append(a)
        return alt_names

    def __unicode__(self):
        return self.name   

    ''' 
    check if point exists for stop
    '''
    def has_point(self):        
        if self.stoplocation_set.all():
            return True
        else:
            return False
        
    has_point.boolean = True

    def get_absolute_url(self):
        return "/stop/%s" % self.slug


#Code, prefix, suffix, aliases
ROUTE_TYPES = (
    (0, "", "", ""), #Ordinary
    (1, "", " Ltd", "L, Limited, Ltd"), #Limited
    (2, "", "", "Extra"), #Ordinary Extra
    (3, "", " Ltd", "L, Limited, Ltd, Extra"), #Limited Extra
    (4, "", "", "Ring"), #Ring Ordinary
    (5, "", " Ltd", "Ring, L, Limited, Ltd"), #Ring Limited
    (6, "C-", " Exp", "C, Express, Exp"), #Express
    (7, "AS-", "", "AS, AC, A"), #AS
    (8, "A-", " Exp", "AS, AC, A, Exp"), #AC Express
    (9, "A-", " Exp", "AS, AC, A, Exp, Extra"), #AC Exp Ext
)

class Route(models.Model):
    code = models.TextField(max_length=255, unique=True) #FIXME: Why is this a TextField??
    slug = models.SlugField(null=True)
    alias = models.TextField(max_length=255, db_index=True)
    from_stop_txt = models.TextField(max_length=500)
    to_stop_txt = models.TextField(max_length=500)
    from_stop = models.ForeignKey(Stop, related_name='routes_from', default=None, null=True, blank=True)
    to_stop = models.ForeignKey(Stop, related_name='routes_to', default=None, null=True, blank=True)
    distance = models.DecimalField(max_digits=3, decimal_places=1)
    stages =  models.IntegerField()
    route_type = models.ForeignKey('RouteType', default=0, null=True, blank=True)
    code3 = models.CharField(max_length=5)

    def get_autocomplete(self):
        '''
        Returns a dict to be used by the autocomplete front-end
        '''
        return {
            'id': self.id,
            'type': 'Route',
            'title': self.alias,
            'url': self.get_absolute_url()
        }

    class Meta:
        ordering = ['code']

    def get_absolute_url(self):
        return "/route/%s/" % self.code

    def __unicode__(self):
        return self.display_name

    @property
    def route_number(self):
        return self.code3.lstrip('0')

    @property
    def display_name(self):
        route_type = int(self.route_type.code)
        prefix = ROUTE_TYPES[route_type][1]
        suffix = ROUTE_TYPES[route_type][2]
        return prefix + self.route_number + suffix

    @property
    def route_type_aliases(self):
        route_type = int(self.route_type.code)
        return ROUTE_TYPES[route_type][3]

    def get_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'alias': self.alias,
            'slug': self.slug,
            'distance': str(self.distance),
            'display_name': self.display_name,
            'url': self.get_absolute_url(),
            'headway': self.headways(),
            'start_stop': self.from_stop.display_name,
            'end_stop': self.to_stop.display_name,
            'start_area': self.from_stop.area.display_name,
            'end_area': self.to_stop.area.display_name,
            'route_type_aliases': self.route_type_aliases
        }

    def areas_passed(self):
        return Area.objects.filter(stop__routedetail__route=self).distinct()
    
    def headways(self, t=None):       
        """ 
        Gives the frequencies of a bus route.
        route.headways() - For current time
        route.headways(t)  - For frequencies at given a day and time, t should be a datetime.datetime() object        
        """
        # get time to be retrieved for        
        if not t:
            t = datetime.datetime.now()
            
        day = t.isoweekday()    
        # get the routeschedules for the route
        scheds = []
        

        #unrs = list(UniqueRoute.objects.filter(route=self))
        #rss = []
        #for unr in unrs:
        #    rss.extend(list(RouteSchedule.objects.filter(unique_route__route=self)))                    
        #print "Rss: ", len(rss)

        for rs in RouteSchedule.objects.filter(unique_route__route=self):
            # if holiday schedule,
            # if 8 in SCHED[rs.schedule_type]:
            # if Holiday.objects.filter(date=t)

            # read route schedule and return headway for time period            
            if day in SCHED[rs.schedule_type]:
                scheds.append(rs)

            #(s.first_from if s.first_from < s.first_to else s.first_to)    
        TIMESPANS = ((None,"06:59:59"),
                     ("07:00:00","10:59:59"),
                     ("11:00:00","16:59:59"),
                     ("17:00:00","19:59:59"),
                     ("20:00:00", None))            

        freqs=[]
        if not scheds:
            return "Its empty!"
        for sch in scheds:
            # Error checking for valid start and stop times.
            # if neither of the start times are mentioned, use 5:00           
            if not sch.first_from and sch.first_to: 
                sch.first_from=sch.first_to=datetime.time(5,0)
            # if neither of the end times are mentioned, use 11:59 pm
            if not sch.last_from and sch.last_to: 
                sch.last_from=sch.last_to=datetime.time(23,59)

            tspan = TIMESPANS
            if (t.time() > sch.first_from or t.time() > sch.first_to) and t.time() < time_of(tspan[0][1]): freqs.append(sch.headway1)
            if t.time() < time_of(tspan[1][1]) and t.time() > time_of(tspan[1][0]): freqs.append(sch.headway2)
            if t.time() < time_of(tspan[2][1]) and t.time() > time_of(tspan[2][0]): freqs.append(sch.headway3)
            if t.time() < time_of(tspan[3][1]) and t.time() > time_of(tspan[3][0]): freqs.append(sch.headway4)
            if (t.time() < sch.last_from or t.time() < sch.last_to) and t.time() > time_of(tspan[4][0]): freqs.append(sch.headway5)
                    
        #avg = float(sum(freqs)/len(freqs))

        #  check here in case we get empty strings or zeroes cropping up
        frequencies = [x for x in freqs if x!=0]        
        if not frequencies:
            return None

        return str(min(frequencies))  + "-" + str(max(frequencies))  if min(frequencies)!=max(frequencies) else str(max(frequencies))

        
               

#'scheds': [ (s.headway1, s.headway2, s.headway3, s.headway4, str(s.unique_route) ) for s in scheds]

class RouteDetail(models.Model):
    route_code = models.TextField()
    route = models.ForeignKey(Route, to_field="code", null=True, blank=True)
    serial = models.PositiveIntegerField()
    stop = models.ForeignKey(Stop, null=True, blank=True)
    stage =  models.NullBooleanField()
    km  = models.DecimalField(null=True, blank=True, max_digits=3, decimal_places=1)

    class Meta:
        verbose_name = 'Route Detail'
        ordering = ['serial'] 

    def __unicode__(self):
        return str(self.route) + " : " + str(self.serial)

    def stop_dir(self):
        return str(self.stop.dbdirection)

class UniqueRoute(models.Model):
    route = models.ForeignKey(Route)
    from_stop_txt = models.CharField(max_length=255)
    to_stop_txt = models.CharField(max_length=255)
    from_stop = models.ForeignKey(Stop, related_name="unique_routes_from")
    to_stop = models.ForeignKey(Stop, related_name="unique_routes_to")
    distance = models.FloatField(blank=True, null=True)
    is_full = models.BooleanField()
#    from_stop.custom_filter_spec = True # this is used to identify the fields which use the custom filter
#    to_stop.custom_filter_spec = True # this is used to identify the fields which use the custom filter
    class Meta:
        verbose_name = 'Atlas'
        verbose_name_plural = 'Atlas'
        
    def __unicode__(self):
        return "%s: %s to %s" % (self.route.alias, self.from_stop_txt, self.to_stop_txt)

    def get_stop_choices(self):
        return Stop.objects.filter(routedetail__route=self.route).order_by('routedetail')


class FuzzyStopMatch(models.Model):
    unr = models.OneToOneField(UniqueRoute)
    checked = models.BooleanField(default=True)

    

class RouteSchedule(models.Model):
    unique_route = models.ForeignKey(UniqueRoute)
    schedule_type = models.CharField(max_length=16)
    busesAM = models.IntegerField(blank=True, null=True)
    busesN = models.IntegerField(blank=True, null=True)
    busesPM = models.IntegerField(blank=True, null=True)
    bus_type = models.CharField(max_length=3, default="SD", blank=True)
    depot_txt = models.CharField(max_length=16, blank=True)
    depot = models.ForeignKey("Depot", null=True, blank=True)
    first_from = models.TimeField(blank=True, null=True)
    last_from = models.TimeField(blank=True, null=True)
    first_to = models.TimeField(blank=True, null=True)
    last_to = models.TimeField(blank=True, null=True)
    runtime1 = models.IntegerField(blank=True, null=True)
    runtime2 = models.IntegerField(blank=True, null=True)
    runtime3 = models.IntegerField(blank=True, null=True)
    runtime4 = models.IntegerField(blank=True, null=True)
    headway1 = models.IntegerField(blank=True, null=True)
    headway2 = models.IntegerField(blank=True, null=True)
    headway3 = models.IntegerField(blank=True, null=True)
    headway4 = models.IntegerField(blank=True, null=True)
    headway5 = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return "%s: %s" % (unicode(self.unique_route), self.schedule_type,)


class RouteType(models.Model):
    code = models.TextField(max_length=50)
    rtype = models.TextField(max_length=50)
    faretype = models.TextField(max_length=10)

    def __unicode__(self):
        return self.rtype   

    class Meta:
        verbose_name = 'Route Type'


class HardCodedRoute(models.Model):
    code = models.TextField(max_length=50)    
    alias = models.TextField(max_length=50)
    faretype = models.TextField(max_length=10)

    class Meta:
        verbose_name = 'Hardcoded Route'

    def __unicode__(self):
        return self.code + " " +self.alias   


class Landmark(models.Model):
    slug = models.SlugField(null=True)
    name = models.TextField(max_length=500, blank=True, null=True)
    stops = models.ManyToManyField(Stop, related_name='is_near_to', blank=True)
    name_mr = models.TextField(max_length=512, blank=True, null=True)
    display_name = models.TextField(blank=True, max_length=255)
    point = models.PointField(blank=True, null=True)
    alt_names = generic.GenericRelation("AlternativeName")

    def __unicode__(self):
        return self.name 


class StopLocation(models.Model):
    stop = models.ForeignKey(Stop)
    point = models.PointField()
    direction = models.CharField(max_length=5, null=True, blank=True, choices=STOP_CHOICES)

    def __unicode__(self):
        return self.stop.name 


class Depot(models.Model):
    code = models.CharField(max_length=5) # should have unique=True ?
    name = models.TextField(max_length=50)
    stop = models.IntegerField()


    def __unicode__(self):
        return self.name 


class Holiday(models.Model):
    date = models.DateField()
    name = models.TextField(max_length=100)
    operating_schedule=models.TextField(max_length=20)

    def __unicode__(self):
        return self.name 
    

ALT_TYPE_CHOICES = (
    ('alt', 'General Alternative Name'),
    ('old', 'Old Name'),
    ('common', 'Common Name')
)

class AlternativeName(models.Model):
    objects = TrigramSearchManager(('name',))
    name = models.CharField(max_length=512)
    name_mr = models.CharField(max_length=512, blank=True)
    typ = models.CharField(max_length=64, choices=ALT_TYPE_CHOICES, default="alt")
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')    

    def __unicode__(self):
        return self.name
