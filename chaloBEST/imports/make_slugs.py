from django.template.defaultfilters import slugify
from mumbai.models import *

def do():
    for cls in [Road, Area, Stop]:
        for obj in cls.objects.all():
            obj.slug = slugify(obj.display_name)
            obj.save()
    for r in Route.objects.all():
        r.slug = r.alias
        r.save()
