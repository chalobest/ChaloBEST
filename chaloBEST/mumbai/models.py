from django.contrib.gis.db import models
from django.contrib import admin


class Area(models.Model):
    a_code = models.IntegerField(primary_key=True)
    areanm = models.TextField(blank=True, max_length=255)
    def __unicode__(self):
        return self.areanm   
    
class Road(models.Model):
    roadcd = models.IntegerField(primary_key=True)
    roadnm = models.TextField(blank=True, max_length=255)
    def __unicode__(self):
        return self.roadnm   


class Fare(models.Model):
    slab = models.DecimalField(max_digits=5, decimal_places=2) 
    ordinary = models.PositiveIntegerField(db_column='ord')
    limited = models.PositiveIntegerField(db_column='ltd')
    express = models.PositiveIntegerField(db_column='exp')
    ac  = models.PositiveIntegerField(db_column='as')
    ac_express = models.PositiveIntegerField(db_column='acexp')
    def __unicode__(self):
        return self.slab   


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
    
    def __unicode__(self):
        return self.stopnm   

class RouteDetails(models.Model):
    rno = models.TextField()
    stopsr = models.PositiveIntegerField()
    stopcd = models.ForeignKey(Stop)
    stage =  models.NullBooleanField()
    km  = models.DecimalField(null=True, blank=True, max_digits=3, decimal_places=1) 
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

    def __unicode__(self):
        return self.routetype   
    

class HardCodedRoutes(models.Model):
    routecode = models.TextField(max_length=50)
    routealias = models.TextField(max_length=50)
    faretype = models.TextField(max_length=10)

    def __unicode__(self):
        return self.routecode + " " +self.routealias   


class AreaAdmin(admin.ModelAdmin):
    pass

class RoadAdmin(admin.ModelAdmin):
    pass

class FareAdmin(admin.ModelAdmin):
    pass

class StopAdmin(admin.ModelAdmin):
    pass

class RouteDetailsAdmin(admin.ModelAdmin):
    pass

class RouteAdmin(admin.ModelAdmin):
    pass

class RouteTypesAdmin(admin.ModelAdmin):
    pass

class HardCodedRoutesAdmin(admin.ModelAdmin):
    pass


admin.site.register(Area, AreaAdmin)
admin.site.register(Road, RoadAdmin)
admin.site.register(Fare,FareAdmin)

admin.site.register(Stop, StopAdmin)
admin.site.register(RouteDetails, RouteDetailsAdmin)
admin.site.register(Route, RouteAdmin)

admin.site.register(RouteTypes, RouteTypesAdmin)
admin.site.register(HardCodedRoutes, HardCodedRoutesAdmin)

