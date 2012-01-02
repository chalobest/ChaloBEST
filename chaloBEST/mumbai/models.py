from django.contrib.gis.db import models
from django.contrib import admin
from django import forms

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
    'MS':[1,2,3,4,5,6], 
    'HOL':[8], 
    'SUN':[7], 
    'MF&HOL':[1,2,3,4,5,8],  
    'SAT':[6], 
    'MF':[1,2,3,4,5], 
    'SH':[7,8], 
    'AD':[1,2,3,4,5,6,7,8], 
    'SAT&SUN':[6,7], 
    'MS&HOL':[1,2,3,4,5,6,8], 
    'FW':[1,2,3,4,5,6,7], 
    'SAT/SH':[6,7,8], 
    'FH':['???'], 
    'SAT&HOL':[6,8], 
    'SAT&SH':[6,7,8], 
    'SAT/SUND&HOL':[6,7,8], 
    'S/H':[7,8], 
    'SAT,SUN&HOL':[6,7,8], 
    '2nd &4th':['???']
    }

class Area(models.Model):
    a_code = models.IntegerField(primary_key=True)
    areanm = models.TextField(blank=True, max_length=255)
    areanm_mr= models.TextField(blank=True, max_length=512)
    def __unicode__(self):
        return self.areanm   
    
class Road(models.Model):
    roadcd = models.IntegerField(primary_key=True)
    roadnm = models.TextField(blank=True, max_length=255)
    roadnm_mr= models.TextField(blank=True, max_length=512)
    def __unicode__(self):
        return self.roadnm   


class Fare(models.Model):
    slab = models.DecimalField(max_digits=5, decimal_places=2) 
    ordinary = models.PositiveIntegerField(db_column='ord')
    limited = models.PositiveIntegerField(db_column='ltd')
    express = models.PositiveIntegerField(db_column='exp')
    ac = models.PositiveIntegerField(db_column='as')
    ac_express = models.PositiveIntegerField(db_column='acexp')
    def __unicode__(self):
        return self.slab   


class Stop(models.Model):
    stopcd = models.IntegerField(primary_key=True)
    stopnm = models.TextField(blank=True, max_length=255)
    stopfl = models.CharField(null=True, blank=True, max_length=5, choices=STOP_CHOICES)
    chowki = models.NullBooleanField(null=True, blank=True) # this is nullable since in the next datafeed , they might have blank to represent a 0.

    roadcd = models.ForeignKey(Road)
    a_code = models.ForeignKey(Area)
    depot = models.TextField(max_length=255) # should actually be a foreign key to a depotMaster,     
    stopnm_mr= models.TextField(blank=True, max_length=512)

    def __unicode__(self):
        return self.stopnm   

class RouteDetails(models.Model):
    rno = models.TextField()
    stopsr = models.PositiveIntegerField()
    stopcd = models.ForeignKey(Stop)
    stage =  models.NullBooleanField()
    km  = models.DecimalField(null=True, blank=True, max_digits=3, decimal_places=1)

    class Meta:
        verbose_name = 'Route Detail'
 
    def __unicode__(self):
        return self.rno   



class Route(models.Model):
    route = models.TextField(max_length=255)
    routealias = models.TextField(max_length=255)
    from_stop = models.TextField(max_length=500,db_column='from')
    to_stop = models.TextField(max_length=500,db_column='to')
    # Ideally they should be ...
    #from_stop = models.ForeignKey(Stop, related_name='from_stop')    
    #to_stop = models.ForeignKey(Stop, related_name='to_stop')
    distance = models.DecimalField(max_digits=3, decimal_places=1) 
    stages =  models.IntegerField()

    def __unicode__(self):
        return self.route   

class UniqueRoute(models.Model):
    route = models.ForeignKey(Route)
    from_stop = models.ForeignKey(Stop, related_name="routes_from")
    to_stop = models.ForeignKey(Stop, related_name="routes_to")
    distance = models.DecimalField(max_digits=3, decimal_places=2)
    is_full = models.BooleanField()

    def __unicode__(self):
        return "%s: %s to %s" % (self.route.routealias, self.from_stop, self.to_stop,)

class RouteSchedule(models.Model):
    unique_route = models.ForeignKey(UniqueRoute)
    schedule_type = models.CharField(max_length=16)
    busesAM = models.IntegerField(blank=True, null=True)
    busesN = models.IntegerField(blank=True, null=True)
    busesPM = models.IntegerField(blank=True, null=True)
    bus_type = models.CharField(max_length=3, default="SD")
    depot = models.ForeignKey("Depot")
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

class RouteTypes(models.Model):
    routecode = models.TextField(max_length=50)
    routetype = models.TextField(max_length=50)
    faretype = models.TextField(max_length=10)

    def __unicode__(self):
        return self.routetype   
    class Meta:
        verbose_name = 'Route Type'

class HardCodedRoutes(models.Model):
    routecode = models.TextField(max_length=50)
    routealias = models.TextField(max_length=50)
    faretype = models.TextField(max_length=10)

    class Meta:
        verbose_name = 'Hardcoded Route'

    def __unicode__(self):
        return self.routecode + " " +self.routealias   


class Landmark(models.Model):
    name = models.TextField(max_length=500, blank=True, null=True)
    stop = models.ManyToManyField(Stop, related_name='is_near_to')
    name_mr = models.TextField(max_length=512, blank=True, null=True)
    def __unicode__(self):
        return self.stop 

class StopLocation(models.Model):
    stop = models.ForeignKey(Stop)
    #point = models.PointField(blank=True, null=True)
    direction = models.CharField(max_length=5, null=True, blank=True, choices=STOP_CHOICES)

    def __unicode__(self):
        return self.stop 

class Depot(models.Model):
    depot_code = models.CharField(max_length=5)
    depot_name = models.TextField(max_length=50)
    stop = models.ForeignKey(Stop, related_name='is_depot_for')
    def __unicode__(self):
        return self.depot_name 


class Holiday(models.Model):
    h_date = models.DateField()
    h_name = models.TextField(max_length=100)
    def __unicode__(self):
        return self.h_name 
    
