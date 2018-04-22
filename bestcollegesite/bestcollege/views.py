# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from model_knn import apply_knn

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


def survey(request):
    template = loader.get_template('survey.html')
    return HttpResponse(template.render())






@csrf_exempt
def submit_survey(request):
    if request.method == 'POST':
        # survey as json
        survey_response = json.loads(request.body.decode('utf-8'))

        # using key to find civil war response
        print ( survey_response )

        ##########################################
        # data var is users survey answers 		 #
        # use this var to decide on best schools #
        # IMPORTANT: when schools are decided, 	 #
        # make a list of their ids IN ORDER		 #
        # 				and return	 			 #
        # See the sample list and response below #
        # This list is used to build the results #
        # url so that page know what schools to  #
        # 			  load data for 			 #
        ##########################################

        #Applying KNN to find the best colleges for the user
        user_input = {}
        user_filters = {}
        unit_ids = apply_knn(user_input, user_filters)

        # for dev testing
        uni_ids = [199193, 199120, 198419, 228778, 217882,
                   187620, 243744, 171100, 216597, 228875]

        # fill zip using value from survey JSON
        # example below
        return HttpResponse( json.dumps( { 'ids' : uni_ids, 'zip' : 28270 } ) )


def results(request):
    params = request.GET.get('ids', '')
    print(params)

    # uni_ids is now a list of the school's ids matching
    # the ids in the dataset
    uni_ids = params.split(',')

    # use uni_ids to pull needed data from the dataset
    # data will likely  be: name, city/state, enrollment/size,
    # anything else desired in the table
    # and latitude/longitude for the map

    template = loader.get_template( 'results.html' )
    return HttpResponse( template.render() )
