from django.contrib.gis import admin
from django import forms
from mumbai.models import *

class RouteScheduleInline(admin.StackedInline):
    model = RouteSchedule
    extras = 0

class AreaAdmin(admin.OSMGeoAdmin):
    list_display = ("code", "name")
    list_editable = ("name",)
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }


class RoadAdmin(admin.OSMGeoAdmin):
    list_display = ("code","name")
    list_editable = ("name",)
    
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }

class FareAdmin(admin.ModelAdmin):
    list_display = ("slab","ordinary","limited","express","ac","ac_express")
    list_editable = ("ordinary","limited","express","ac","ac_express")
    
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }
    
class UniqueRouteAdmin(admin.ModelAdmin):
    inlines = [RouteScheduleInline]


class StopForm(forms.ModelForm):
    
    class Meta:
        model = Stop
        

class StopAdmin(admin.OSMGeoAdmin):
    list_display = ("code","name","name_mr", "road","area","dbdirection","depot","chowki" )
    list_editable = ("name", "name_mr","dbdirection","depot","chowki")
    search_fields = ("code",'name', 'depot')
    ordering = ('name',)
    list_per_page = 20

    fieldsets = (
        (None, {
            'fields': ('name', 'area', 'road')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('code', 'chowki', 'depot')
        }),
    )
    form = StopForm
    # For mapping widget
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }


class RouteDetailAdmin(admin.ModelAdmin):
    list_display = ("route","serial","stop","stage","km")
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }
    

class RouteAdmin(admin.ModelAdmin):
    list_display = ("alias","code","from_stop","to_stop","distance","stages")
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }
    

class RouteTypeAdmin(admin.ModelAdmin):
    list_display = ("code","rtype","faretype")    
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }
    

class HardCodedRouteAdmin(admin.ModelAdmin):
    list_display = ("code","alias","faretype")
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }
    
class LandmarkAdmin(admin.ModelAdmin):
    list_display = ("name", "name_mr")
    #list_editable = ("name","name_mr")
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }

class StopLocationAdmin(admin.OSMGeoAdmin):
    list_display = ("stop", "direction", "point")

    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }

class DepotAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "stop")
    #list_editable = ("name",) 
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }


class HolidayAdmin(admin.ModelAdmin):
    list_display = ("date", "name") 
    list_editable = ("name",) 
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }



admin.site.register(Area, AreaAdmin)
admin.site.register(Road, RoadAdmin)
admin.site.register(Fare,FareAdmin)

admin.site.register(Stop, StopAdmin)
admin.site.register(RouteDetail, RouteDetailAdmin)
admin.site.register(Route, RouteAdmin)

admin.site.register(RouteType, RouteTypeAdmin)
admin.site.register(HardCodedRoute, HardCodedRouteAdmin)

admin.site.register(Landmark, LandmarkAdmin )
admin.site.register(Depot,DepotAdmin)
admin.site.register(Holiday,HolidayAdmin)
admin.site.register(StopLocation,StopLocationAdmin)

admin.site.register(UniqueRoute, UniqueRouteAdmin)
