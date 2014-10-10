from django.shortcuts import redirect
from django.shortcuts import render_to_response
from ox.django.shortcuts import get_object_or_404_json, render_to_json_response
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
import json
from os.path import join
from gtfs.gtfs_export import *

def index(request):
    return render_to_response('index.html', {} )

def tweety(request):
    f = open('/tmp/twittercallback.log','a')
    f.write(str(request));     
    f.write("\n")
    f.close()
    return render_to_json_response({'RECEIVED':'OK'} )


