from django.template.defaultfilters import slugify
from mumbai.models import *

def do():
    for cls in [Road, Area, Stop]:
        for obj in cls.objects.all():
            slug = slugify(obj.display_name)
            if cls.objects.filter(slug=slug).count() > 1:
                slug += "2"
            obj.slug = slug
            obj.save()
    for r in Route.objects.all():
        r.slug = r.alias
        r.save()
