from django.contrib.gis.db import models

class Area(models.Model):
    a_code = models.IntegerField(primary_key=True)
    areanm = models.TextField(blank=True, max_length=255)
    
class Road(models.Model):
    roadcd = models.IntegerField(primary_key=True)
    roadnm = models.TextField(blank=True, max_length=255)

class Fare(models.Model):
    slab = models.DecimalField(max_digits=5, decimal_places=2) 
    ordinary = models.PositiveIntegerField(db_column='ord')
    limited = models.PositiveIntegerField(db_column='ltd')
    express = models.PositiveIntegerField(db_column='exp')
    ac  = models.PositiveIntegerField(db_column='as')
    ac_express = models.PositiveIntegerField(db_column='acexp')

STOP_CHOICES = ( ('U','Up'),
                 ('D', 'Down'),
                 )

class Stop(models.Model):
    stopcd = models.IntegerField(primary_key=True)
    stopnm = models.TextField(blank=True, max_length=255)
    stopfl = models.CharField(null=True, blank=True, max_length=5, choices=STOP_CHOICES)
    chowki = models.NullBooleanField(null=True, blank=True) # this is nullable since in the next datafeed , they might have blank to represent a 0.
    roadcd = models.ForeignKey(Road)
    a_code = models.ForeignKey(Area)
    depot = models.TextField(max_length=255) # should actually be a foreign key to a depotMaster, 
    
class RouteDetails(models.Model):
    rno = models.TextField()
    stopsr = models.PositiveIntegerField()
    stopcd = models.ForeignKey(Stop)
    stage =  models.BooleanField()
    km  = models.DecimalField(max_digits=3, decimal_places=1) 



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

######j:  A logic to find out the routetype/ route code in every bus.
#    1. Separate the route code into the first 3 digits, and the ending
#    2. i.e. |routecode|    becomes      | routenum | routetypecode|
#            |     8011|                 |  801     | LTD          |
#    3. while populating the routetypecode, we need to a script to search in both hardcoded routes as well as the routecode in Route 
#    4.  then this parsing happens only at data loading stage, 

class RouteTypes(models.Model):
    routecode = models.TextField(max_length=50)
    routetype = models.TextField(max_length=50)
    faretype = models.TextField(max_length=10)
    
class HardCodedRoutes(models.Model):
    routecode = models.TextField(max_length=50)
    routealias = models.TextField(max_length=50)
    faretype = models.TextField(max_length=10)
