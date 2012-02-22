from django.template.defaultfilters import slugify
from mumbai.models import *


def clear_slugs():
    for cls in [Road, Area, Stop]:
        for obj in cls.objects.all():
            obj.slug = ''
            obj.save()

def do():
    for cls in [Road, Area, Stop]:
        slugIncrements = {}
        # theseSlugs = []
        for obj in cls.objects.all():
            slug = slugify(obj.display_name)
            if slug in slugIncrements:
                slugIncrements[slug] += 1
                finalSlug = slug + "_" + str(slugIncrements[slug])
            else:
                slugIncrements.update({slug: 1})
                finalSlug = slug               
            obj.slug = finalSlug
            obj.save()
    for r in Route.objects.all():
        r.slug = r.alias
        r.save()
