from django.contrib import admin
from django import forms
from mumbai.models import *

class AreaAdmin(admin.ModelAdmin):
    list_display = ("a_code", "areanm")
    list_editable = ("areanm",)
    

class RoadAdmin(admin.ModelAdmin):
    list_display = ("roadcd","roadnm")
    list_editable = ("roadnm",)

class FareAdmin(admin.ModelAdmin):
    list_display = ("slab","ordinary","limited","express","ac","ac_express")
    list_editable = ("ordinary","limited","express","ac","ac_express")
    

class StopForm(forms.ModelForm):
    
    class Meta:
        model = Stop
        

class StopAdmin(admin.ModelAdmin):
    list_display = ("stopcd","stopnm", "roadcd","a_code","stopfl","depot","chowki")
    list_editable = ("stopnm", "roadcd","a_code","stopfl","depot","chowki")
    search_fields = ("stopcd",'stopnm', 'depot')
    ordering = ('-stopnm',)

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
    

class RouteAdmin(admin.ModelAdmin):
    list_display = ("routealias","route","from_stop","to_stop","distance","stages")
    

class RouteTypesAdmin(admin.ModelAdmin):
    list_display = ("routecode","routetype","faretype")    
    

class HardCodedRoutesAdmin(admin.ModelAdmin):
    list_display = ("routecode","routealias","faretype")
    
class AreaAdmin(admin.ModelAdmin):
    list_display = ("a_code", "areanm")
    list_editable = ("areanm",)


admin.site.register(Area, AreaAdmin)
admin.site.register(Road, RoadAdmin)
admin.site.register(Fare,FareAdmin)

admin.site.register(Stop, StopAdmin)
admin.site.register(RouteDetails, RouteDetailsAdmin)
admin.site.register(Route, RouteAdmin)

admin.site.register(RouteTypes, RouteTypesAdmin)
admin.site.register(HardCodedRoutes, HardCodedRoutesAdmin)

