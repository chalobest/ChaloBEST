# Create your views here.
from django.core.management import setup_environ
import settings
setup_environ(settings)
from users.models import UserProfile
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
import django.utils.simplejson as json
import os
import urllib2
#from users.models import *
from StringIO import StringIO
#from django.http import HttpResponse
from django.contrib.auth.models import User


def getsmsfeed(request):
	current_user = request.user
	print current_user	
	users = user.objects.all()

	apireq = urllib2.Request('http://sms.chalobest.in/messages_json/?phone_no='+mobilenumber)
        apires = urllib2.urlopen(apireq)
	try:
                        #jsonres = json.dumps(apires,sort_keys=True)
                        ##print jsonres.__class__
                        #print apires
	        jstr = json.load(apires)
                l = (json.dumps(jstr,sort_keys=True)).split("}")
                        #print l
                sjstr = sorted(l, key=lambda l:l[0])
                        #print sjstr[0]['datetime']
                        #k = [i for i, j, k in jstr[1]]
                print sjstr[-5:]

                        #print jstr.get('text')
                        #print l.__class__
        except ValueError,e:
                print e


