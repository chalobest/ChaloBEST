from django.contrib.gis.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


LANGUAGE_CHOICES = (
    ('en', 'English'),
    ('ma', 'Marathi'),
    ('hi', 'Hindi'),
)

ALTERNATIVE_NAME_TYPES = (
    ('colloquial', 'Colloquial'),
    ('official', 'Official'),
    ('historical', 'Historical'),
    ('other', 'Other'),
)

DIRECTION_CHOICES = (
    ('up', 'Up'),
    ('down', 'Down'),
    ('ring', 'Ring'),
)

class Area(models.Model):
    AreaCode = models.CharField(max_length=512)
    AreaName = models.CharField(max_length=512)
    polygon = models.PolygonField(blank=True, null=True)

    def __unicode__(self):
        return self.AreaName   


class Stop(models.Model):
    _id = models.IntegerField(unique=True, db_index=True, primary_key=True)
    stopname = models.CharField(max_length=512)
    stopnameid = models.CharField(max_length=512)
#	areacode = models.IntegerField()
    area = models.ForeignKey("Area")
#	area = models.CharField(max_length=512)
    point = models.PointField(blank=True, null=True)
#	lat = models.DecimalField(max_digits=4, decimal_places=2) #max_digits -> 999.99
#	lon = models.DecimalField(max_digits=5, decimal_places=2)
    buses = models.ManyToManyField("Route")
#	buses = models.CharField(max_length=512)
#	landmark = models.CharField(max_length=512)
#	areastopnamelandmark = models.CharField(max_length=512)
#	noofbuses = models.IntegerField()

    def __unicode__(self):
	    return self.stopname

class Landmark(models.Model):
    stop = models.ForeignKey(Stop)
    point = models.PointField(blank=True, null=True)
#	stopcode = models.CharField(max_length=512)    
    landmark = models.CharField(max_length=512)
    
    def __unicode__(self):
        return self.landmark

class StopLocation(models.Model):
    _id = models.IntegerField(unique=True, db_index=True, primary_key=True)
    stopid  = models.ForeignKey(Stop) 
#	stopnameid = models.CharField(max_length=512)
#	landmark = models.CharField(max_length=512)
    pointu = models.PointField(blank=True, null=True)
    pointd = models.PointField(blank=True, null=True)    
    point = models.PointField(blank=True, null=True)

#	lat = models.PointField(blank=True, null=True)
#	lon = models.PointField(blank=True, null=True)
    busesup = models.ManyToManyField("Route" , related_name="buses_up")
#	busesup  = models.CharField(max_length=512)
    busesdown = models.ManyToManyField("Route", related_name="buses_dn")
#	stopcode  = models.CharField(max_length=512)

    def __unicode__(self):
        return self.stopnameid

'''
class StopsCollected(models.Model):
	area = models.CharField(max_length=512)
	stopname = models.CharField(max_length=512)
	landmark = models.CharField(max_length=512)
	buses_up = models.CharField(max_length=512)
    pointu = models.PointField(blank=True, null=True)
    pointd = models.PointField(blank=True, null=True)
#	latu = models.CharField(max_length=512)
#	lonu = models.CharField(max_length=512)
	buses_dn = models.CharField(max_length=512)
	latd = models.CharField(max_length=512)
	lond = models.CharField(max_length=512)
	displayname = models.CharField(max_length=512)
#	arealat = models.CharField(max_length=512)
#	arealon = models.CharField(max_length=512)
#	areabest = models.CharField(max_length=512)
#	stopcode = models.ForeignKey('Stop', related_name="code")  
    area = models.ForeignKey("Area")
#	areacode = models.CharField(max_length=512)
	stopnameid = models.ForeignKey('Stop', related_name="nameid") 

	def __unicode__(self):
		return self.stopname
'''

class Stopcode(models.Model):
    _id = models.IntegerField(unique=True, db_index=True, primary_key=True)
    stopcode = models.CharField(max_length=512)
    stopid = models.ForeignKey(Stop) 
#	landmark = models.CharField(max_length=512)

    def __unicode__(self):
        return self.stopcode


class Atlas(models.Model):
    atlas_id = models.IntegerField(unique=True, db_index=True, primary_key=True)
    route = models.ForeignKey("Route")
#	RouteCode = models.CharField(max_length=512)
#	FirstStop = models.CharField(max_length=512)
    FirstFrom = models.DecimalField(max_digits=4, decimal_places=2)
    FirstTo = models.DecimalField(max_digits=4, decimal_places=2)
#	LastStop = models.CharField(max_length=512)
    LastFrom = models.DecimalField(max_digits=4, decimal_places=2)
    LastTo = models.DecimalField(max_digits=4, decimal_places=2)
    am = models.DecimalField(max_digits=4, decimal_places=2)
    noon = models.DecimalField(max_digits=4, decimal_places=2)
    pm = models.DecimalField(max_digits=4, decimal_places=2)
    schedule = models.CharField(max_length=255)
    firststopserial = models.IntegerField()
    laststopserial = models.IntegerField()
#	firststopnameid = models.CharField(max_length=512)
#	laststopnameid = models.CharField(max_length=512)
    firststopid = models.ForeignKey(Stop, blank=True, null=True, related_name="first_stop") 
    laststopid = models.ForeignKey(Stop, blank=True, null=True, related_name="last_stop")  

    def __unicode__(self):
        return "%s %s" %(self.firststopid, self.laststopid)

class Route(models.Model):
    _id = models.IntegerField(unique=True, db_index=True, primary_key=True)
    routeCode = models.CharField(max_length=512)
    laststop = models.IntegerField()
    busno = models.CharField(max_length=512)
    firststopid = models.ForeignKey(Stop, related_name="stop_up")  
    laststopid = models.ForeignKey(Stop, related_name="stop_dn") 
    fstopname = models.CharField(max_length=512)
    lstopname = models.CharField(max_length=512)

    def __unicode__(self):
        return self.routeCode
	

class RouteDetail(models.Model):
    _id = models.IntegerField(unique=True, db_index=True, primary_key=True)
    routeCode = models.CharField(max_length=512)
    stopSerial = models.IntegerField()
#	stopCode = models.IntegerField() #FIXME
    stage = models.CharField(max_length=512)
    km = models.CharField(max_length=512)
    busno = models.IntegerField()
    stoplocationidup = models.ForeignKey("StopLocation", related_name="route_up")
    stoplocationiddown = models.ForeignKey("StopLocation", related_name="route_dn")
    stopid = models.ForeignKey(Stop)  

    def __unicode__(self):
        return self.routeCode

class Frequency(models.Model):
    _id = models.IntegerField(unique=True, db_index=True, primary_key=True)
    startheadway = models.IntegerField()
    endheadway = models.IntegerField()
    frequency = models.IntegerField()
    startdayweek = models.IntegerField()
    enddayweek = models.IntegerField()
#	firststopserial = models.IntegerField()
#	laststopserial = models.IntegerField()
    holiday = models.CharField(max_length=512)
#	routecode = models.CharField(max_length=512)
#	firststopid = models.ForeignKey(Stop)  
#	laststopid = models.ForeignKey(Stop)   
#	atlasfirststop = models.CharField(max_length=512)
#	atlaslaststop = models.CharField(max_length=512)
    atlas_id = models.ForeignKey(Atlas)  


    def __unicode__(self):
        return "frequency"


class BestAtlas(models.Model):
    RouteCode = models.CharField(max_length=512)
    BusNo = models.CharField(max_length=512)
    FirstStop = models.CharField(max_length=512)
    FirstFrom = models.CharField(max_length=512)
    LastFrom = models.CharField(max_length=512)
    Laststop = models.CharField(max_length=512)
    FirstTo = models.CharField(max_length=512)
    LastTo = models.CharField(max_length=512)
    Am = models.CharField(max_length=512)
    Noon = models.CharField(max_length=512)
    Pm = models.CharField(max_length=512)
    Schedule = models.CharField(max_length=512)

    def __unicode__(self):
        return self.RouteCode

class BestStopMaster(models.Model):
    StopCode = models.CharField(max_length=512)
    StopName = models.CharField(max_length=512)
    STOPFL = models.CharField(max_length=512)
    RoadCode = models.CharField(max_length=512)
    AreaCode = models.CharField(max_length=512)
    DEPOT = models.CharField(max_length=512)

    def __unicode__(self):
        return self.StopName

class ScheduleLookup(models.Model):
    schedule = models.CharField(max_length=512)
    startday = models.IntegerField()
    endday = models.IntegerField()
    holiday = models.CharField(max_length=512)

    def __unicode__(self):
        return self.schedule

class BestRouteDetails(models.Model):
    RouteCode = models.CharField(max_length=512) 
    StopSerial = models.CharField(max_length=512) 
    StopCode = models.CharField(max_length=512) 
    Stage = models.CharField(max_length=512) 
    Km = models.CharField(max_length=512) 


    def __unicode__(self):
        return self.RouteCode

class BestAreaMaster(models.Model):
    AreaCode = models.CharField(max_length=512)
    AreaName = models.CharField(max_length=512)
	

    def __unicode__(self):
        return self.AreaName
