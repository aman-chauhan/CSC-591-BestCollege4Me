# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader


def index( request ):
	template = loader.get_template( 'index.html' )
	return HttpResponse( template.render() )

def survey( request ):
	template = loader.get_template( 'survey.html' )
	return HttpResponse( template.render() )

def results( request ):
	template = loader.get_template( 'results.html' )
	return HttpResponse( template.render() )
