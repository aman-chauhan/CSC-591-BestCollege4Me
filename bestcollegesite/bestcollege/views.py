# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .model_knn import apply_knn

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.views.decorators.csrf import csrf_exempt
import json

def get_states_from_regions( regions ):
    region_map = { 'south' : ['Arkansas', 'North Carolina', 'South Carolina', 'Georgia', 'Florida', 'Alabama', 'Mississippi', 'Kentucky', 'Tennessee', 'Louisiana', 'Virginia', 'West Virginia'],
  'newEngland' : ['New Hampshire', 'Connecticut', 'Massachusets', 'Vermont', 'Rhode Island', 'Maine'],
  'midAtlantic' : ['Delaware', 'Maryland', 'New Jersey', 'New York', 'Pennsylvania'],
  'midwest' : ['Illinois', 'Indiana', 'Iowa', 'Kansas', 'Michigan', 'Minnesota', 'Missouri', 'Nebraska', 'North Dakota', 'Ohio', 'South Dakota', 'Wisconsin'],
  'southwest' : ['Arizona', 'New Mexico', 'Oklahoma', 'Texas'],
  'west' : ['Alaska', 'Colorado', 'California', 'Hawaii', 'Idaho', 'Montana', 'Nevada', 'Oregon', 'Utah', 'Washington', 'Wyoming'] }
    states = []
    for region in regions:
        for state in region_map[region]:
            states.append( state )

    return states

def get_demographic( survey_dem, dem_key ):
    demographic_mapping = { 'White' : 'UGDS_WHITE', 'Black' : 'UGDS_BLACK', 'Hispanic' : 'UGDS_HISP', 'Asian' : 'UGDS_ASIAN', 'Asian Pacific Islander' : 'UGDS_AIAN', 'Tribal' : 'UGDS_NHPI' }    
    if survey_dem is not None and survey_dem in demographic_mapping and demographic_mapping[survey_dem] == dem_key:
        return 1
    else:
        return 0

def get_income_range( survey_income, income_key ):
    income_mapping = { '< $30,000' : 'INC_PCT_LO', '$30,00 - $48,000' : 'INC_PCT_M1', '$48,000 - $75,000' : 'INC_PCT_M2',
                    '$75,000 - $110,000' : 'INC_PCT_H1', '> $110,000' : 'INC_PCT_H2' }

    if income_mapping[survey_income] == income_key:
        return 1
    else:
        return 0

def get_student_body_size( survey_school_size ):
    size_mapping = { 'Very small' : [0, 1000], 'Small' : [1000, 2500], 'Medium' : [2500, 10000], 'Large' : [10000, 100000] }
    return size_mapping[survey_school_size]

def get_historic( survey_historic, historic_key ):
    if survey_historic is not None and survey_historic == historic_key:
        return 1
    else:
        return 0

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

        sat = None
        if 'SAT_AVG' in survey_response['testScores']:
            sat = survey_response['testScores']['SAT_AVG']

        act = None
        if 'ACTCMID' in survey_response['testScores']:
            act = survey_response['testScores']['ACTCMID'] 

        dem = None
        if 'demographicType' in survey_response:
            dem = survey_response['demographicType']

        #Applying KNN to find the best colleges for the user
        user_input = { 'HIGHDEG' : 4, 'SAT_AVG' : sat, 'ACTCMID' : act, 'UGDS_WHITE' : get_demographic( dem, 'UGDS_WHITE' ), 'UGDS_BLACK' : get_demographic( dem, 'UGDS_BLACK' ),
            'UGDS_HISP' : get_demographic( dem, 'UGDS_HISP' ), 'UGDS_ASIAN' : get_demographic( dem, 'UGDS_ASIAN' ), 'UGDS_AIAN' : get_demographic( dem, 'UGDS_AIAN' ),
            'UGDS_NHPI' : get_demographic( dem, 'UGDS_NHPI' ), 'UGDS_2MOR' : 0, 'UGDS_NRA' : 0, 'UGDS_UNKN' : 0,
            'UG25ABV' : survey_response['UG25ABV'], 'PPTUG_EF' : survey_response['PPTUG_EF'], 'INC_PCT_LO' : get_income_range( survey_response['householdIncome'], 'INC_PCT_LO' ),
            'INC_PCT_M1' : get_income_range( survey_response['householdIncome'], 'INC_PCT_M1' ), 'INC_PCT_M2' : get_income_range( survey_response['householdIncome'], 'INC_PCT_M2' ),
            'INC_PCT_H1' : get_income_range( survey_response['householdIncome'], 'INC_PCT_H1' ), 'INC_PCT_H2' : get_income_range( survey_response['householdIncome'], 'INC_PCT_H2' ),
            'PAR_ED_PCT_1STGEN' : None, 'C150_4' : 1, 'PCIP14' : 1 }

        #semesterTuition
        #stateSchool

        tuition_in = None
        tuition_out = None
        if survey_response['stateSchool'] == 'inState':
            tuition_in = [0, survey_response['semesterTuition']]
        elif survey_response['stateSchool'] == 'outOfState':
            tuition_out = [0, survey_response['semesterTuition']]
        else:
            tuition_in = [0, survey_response['semesterTuition']]
            tuition_out = [0, survey_response['semesterTuition']]

        men_only = None
        women_only = None
        if survey_response['genderExclusive']:
            if survey_response['gender'] == 'male':
                men_only = 1
            elif survey_response['gender'] == 'female':
                women_only = 1

        states = []
        if 'region' in survey_response:
            states = get_states_from_regions( survey_response['region'] )
        else:
            states.append( survey_response['STABBR'] )

        historic_type = None
        if 'historicType' in survey_response:
            historic_type = survey_response['historicType']


        user_filters = { 'ADM_RATE' : [survey_response['acceptanceRate'] / 100.0, 1], 'UGDS' : get_student_body_size( survey_response['studentBodySize'] ),
        'TUITIONFEE_IN' : tuition_in, 'TUITIONFEE_OUT' : tuition_out, 'STABBR' : states, 'MAIN' : survey_response['MAIN'], 'CONTROL' : survey_response['CONTROL'],
        'RELAFFIL' : None, 'DISTANCEONLY' : survey_response['DISTANCEONLY'], 'HBCU': get_historic( historic_type, 'HBCU' ), 'PBI': get_historic( historic_type, 'PBI' ),
        'ANNHI': get_historic( historic_type, 'ANNHI' ), 'HSI': get_historic( historic_type, 'HSI' ), 'NANTI': get_historic( historic_type, 'NANTI' ),
        'MENONLY': men_only, 'WOMENONLY': women_only, 'CIP14BACHL': 1, 'GRAD_DEBT_MDN10YR': [0,survey_response['monthlyLoans']] }

        unit_ids = apply_knn(user_input, user_filters)

        # for dev testing
        uni_ids = [199193, 139959, 198419, 228778, 217882, 100858, 243744, 171100, 216597, 228875]

        # fill zip using value from survey JSON
        # example below
        return HttpResponse( json.dumps( { 'ids' : uni_ids, 'zip' : int ( survey_response['zipCode'] ) } ) )


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

@csrf_exempt
def sort_results( request ):
    # should be map of nightlife scores
    # keys are unitids of schools
    if request.method == 'POST':
        # survey as json
        nightlife_scores = json.loads( request.body.decode( 'utf-8' ) )
        print ( nightlife_scores )

    # sorting done here

    # fake new sorted map
    unit_ids = [139959, 228875, 198419, 199193, 228778, 100858, 217882, 243744, 171100, 216597]
    return HttpResponse( json.dumps( { 'ids' : unit_ids } ) )