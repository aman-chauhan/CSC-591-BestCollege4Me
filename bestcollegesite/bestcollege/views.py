# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader


def index( request ):
	template = loader.get_template( 'index.html' )
	return HttpResponse( template.render() )

# Create your views here.
