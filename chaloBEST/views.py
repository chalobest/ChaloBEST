from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import json
from os.path import join


def index(request):
    return render_to_response('index.html', {} )
