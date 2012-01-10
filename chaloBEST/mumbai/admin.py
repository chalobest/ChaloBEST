from django.contrib import admin
from django import forms
from mumbai.models import *

class RouteScheduleInline(admin.StackedInline):
    model = RouteSchedule

class AreaAdmin(admin.ModelAdmin):
    list_display = ("a_code", "areanm")
    list_editable = ("areanm",)
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }


class RoadAdmin(admin.ModelAdmin):
    list_display = ("roadcd","roadnm")
    list_editable = ("roadnm",)
    
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
        

class StopAdmin(admin.ModelAdmin):
    list_display = ("stopcd","stopnm", "roadcd","a_code","stopfl","depot","chowki")
    list_editable = ("stopnm", "roadcd","a_code","stopfl","depot","chowki")
    search_fields = ("stopcd",'stopnm', 'depot')
    ordering = ('stopnm',)
    list_per_page = 20

    fieldsets = (
        (None, {
            'fields': ('stopnm', 'a_code', 'roadcd')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('stopcd', 'chowki', 'depot')
        }),
    )
    form = StopForm
    # For mapping widget
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }


class RouteDetailsAdmin(admin.ModelAdmin):
    list_display = ("rno","stopsr","stopcd","stage","km")
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }
    

class RouteAdmin(admin.ModelAdmin):
    list_display = ("alias","code","from_stop","to_stop","distance","stages")
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }
    

class RouteTypesAdmin(admin.ModelAdmin):
    list_display = ("routecode","routetype","faretype")    
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }
    

class HardCodedRoutesAdmin(admin.ModelAdmin):
    list_display = ("routecode","routealias","faretype")
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }
    
class LandmarkAdmin(admin.ModelAdmin):
    list_display = ("name", "name_mr")
    list_editable = ("name_mr",)
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }

class StopLocationAdmin(admin.ModelAdmin):
    list_display = ("stop", "direction")
    #list_editable = ("name","name_mr")
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }

class DepotAdmin(admin.ModelAdmin):
    list_display = ("depot_code", "depot_name", "stop")
    list_editable = ("depot_name",) 
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }


class HolidayAdmin(admin.ModelAdmin):
    list_display = ("h_date", "h_name") 
    list_editable = ("h_name",) 
    formfield_overrides = {
        models.TextField: {'widget': forms.TextInput},
    }



admin.site.register(Area, AreaAdmin)
admin.site.register(Road, RoadAdmin)
admin.site.register(Fare,FareAdmin)

admin.site.register(Stop, StopAdmin)
admin.site.register(RouteDetails, RouteDetailsAdmin)
admin.site.register(Route, RouteAdmin)

admin.site.register(RouteTypes, RouteTypesAdmin)
admin.site.register(HardCodedRoutes, HardCodedRoutesAdmin)

admin.site.register(Landmark, LandmarkAdmin )
admin.site.register(Depot,DepotAdmin)
admin.site.register(Holiday,HolidayAdmin)
admin.site.register(StopLocation,StopLocationAdmin)

admin.site.register(UniqueRoute, UniqueRouteAdmin)
