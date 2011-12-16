from django.contrib import admin
from django import forms
from mumbai.models import *

class AreaAdmin(admin.ModelAdmin):
    list_display = ("a_code", "areanm")
    

class RoadAdmin(admin.ModelAdmin):
    list_display = ("roadcd","roadnm")
    

class FareAdmin(admin.ModelAdmin):
    list_display = ("slab","ordinary","limited","express","ac","ac_express")
    

class StopForm(forms.ModelForm):
    
    class Meta:
        model = Stop
        

class StopAdmin(admin.ModelAdmin):
    list_display = ("stopcd","stopnm", "roadcd","a_code","stopfl","depot","chowki")
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
    #formfield_overrides = {
    #    models.TextField: {'widget': RichTextEditorWidget},
    #}


class RouteDetailsAdmin(admin.ModelAdmin):
    list_display = ("rno","stopsr","stopcd","stage","km")
    

class RouteAdmin(admin.ModelAdmin):
    list_display = ("routealias","route","from_stop","to_stop","distance","stages")
    

class RouteTypesAdmin(admin.ModelAdmin):
    list_display = ("routecode","routetype","faretype")    
    

class HardCodedRoutesAdmin(admin.ModelAdmin):
    list_display = ("routecode","routealias","faretype")
    


admin.site.register(Area, AreaAdmin)
admin.site.register(Road, RoadAdmin)
admin.site.register(Fare,FareAdmin)

admin.site.register(Stop, StopAdmin)
admin.site.register(RouteDetails, RouteDetailsAdmin)
admin.site.register(Route, RouteAdmin)

admin.site.register(RouteTypes, RouteTypesAdmin)
admin.site.register(HardCodedRoutes, HardCodedRoutesAdmin)

