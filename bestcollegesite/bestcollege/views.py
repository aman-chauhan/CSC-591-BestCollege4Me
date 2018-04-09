# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.views.decorators.csrf import csrf_exempt
import json


def index( request ):
	template = loader.get_template( 'index.html' )
	return HttpResponse( template.render() )

def survey( request ):
	template = loader.get_template( 'survey.html' )
	return HttpResponse( template.render() )

@csrf_exempt
def submit_survey( request ):
	if request.method == 'POST':
		#survey as json
		data = json.loads( request.body.decode( 'utf-8' ) )

		#using key to find civil war response
		print data['civilwar']

		uni_ids = [1, 2, 3, 4, 5]
		return HttpResponse( json.dumps( uni_ids ) )

def results( request ):
	template = loader.get_template( 'results.html' )
	return HttpResponse( template.render() )
