# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .model_knn import apply_knn
from .model_topsis import perform_topsis

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.views.decorators.csrf import csrf_exempt
import json

survey_response = {
    'winter' : '40.0',
    'spring' : '65.0',
    'summer' : '80.0',
    'fall' : '60'
}

religion_map = {
    "American Evangelical Lutheran Church" : 22,
    "African Methodist Episcopal Zion Church" : 24,
    "Assemblies of God Church" : 24,
    "Brethren Church" : 28,
    "Roman Catholic" : 30,
    "Wisconsin Evangelical Lutheran Synod" : 33,
    "Christ and Missionary Alliance Church" : 34,
    "Christian Reformed Church" : 35,
    "Evangelical Congregational Church" : 36,
    "Evangelical Covenant Church of America" : 37,
    "Evangelical Free Church of America" : 38,
    "Evangelical Lutheran Church" : 39,
    "International United Pentecostal Church" : 40,
    "Free Will Baptist Church" : 41,
    "Interdenominational" : 42,
    "Mennonite Brethren Church" : 43,
    "Moravian Church" : 44,
    "North American Baptist" : 45,
    "Pentecostal Holiness Church" : 47,
    "Christian Churches and Churches of Christ" : 48,
    "Reformed Church in America" : 49,
    "Episcopal Church, Reformed" : 50,
    "African Methodist Episcopal" : 51,
    "American Baptist" : 52,
    "American Lutheran" : 53,
    "Baptist" : 54,
    "Christian Methodist Episcopal" : 55,
    "Church of God" : 57,
    "Church of Brethren" : 58,
    "Church of the Nazarene" : 59,
    "Cumberland Presbyterian" : 60,
    "Christian Church (Disciples of Christ)" : 61,
    "Free Methodist" : 64,
    "Friends" : 65,
    "Presbyterian Church (USA)" : 66,
    "Lutheran Church in America" : 67,
    "Lutheran Church - Missouri Synod" : 68,
    "Mennonite Church" : 69,
    "United Methodist" : 71,
    "Protestant Episcopal" : 73,
    "Churches of Christ" : 74,
    "Southern Baptist" : 75,
    "United Church of Christ" : 76,
    "Protestant, not specified" : 77,
    "Multiple Protestant Denomination" : 78,
    "Other Protestant" : 79,
    "Jewish" : 80,
    "Reformed Presbyterian Church" : 81,
    "United Brethren Church" : 84,
    "Missionary Church Inc" : 87,
    "Undenominational" : 88,
    "Wesleyan" : 89,
    "Greek Orthodox" : 91,
    "Russian Orthodox" : 92,
    "Unitarian Universalist" : 93,
    "Latter Day Saints (Mormon Church)" : 94,
    "Seventh Day Adventists" : 95,
    "The Presbyterian Church in America" : 97,
    "Other (none of the above)" : 99,
    "Original Free Will Baptist" : 100,
    "Ecumenical Christian" : 101,
    "Evangelical Christian" : 102,
    "Presbyterian" : 103
}

def get_states_from_regions( regions, home_state ):
    region_map = { 'south' : ['AR', 'NC', 'SC', 'GA', 'FL', 'AL', 'MS', 'KY', 'TN', 'LA', 'VA', 'WV'],
  'newEngland' : ['NH', 'CT', 'MA', 'VT', 'RI', 'ME'],
  'midAtlantic' : ['DE', 'MD', 'NJ', 'NY', 'PA'],
  'midwest' : ['IL', 'IN', 'IA', 'KS', 'MI', 'MN', 'MO', 'NE', 'ND', 'OH', 'SD', 'WI'],
  'southwest' : ['AZ', 'NM', 'OK', 'TX'],
  'west' : ['AK', 'CO', 'CA', 'HI', 'ID', 'MT', 'NV', 'OR', 'UT', 'WA', 'WY'] }
    states = []
    for region in regions:
        for state in region_map[region]:
            if home_state != state:
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
    size_mapping = { 'Very small' : [0, 1000], 'Small' : [1000, 2500], 'Medium' : [2500, 10000], 'Large' : [10000, 100000], "Don't Care": [] }
    return size_mapping[survey_school_size]

def get_historic( survey_historic, historic_key ):
    if survey_historic is not None and survey_historic == historic_key:
        return 1
    else:
        return 0

def get_numeric_val(response, key):
    if response[key]:
        if '.' in response[key]:
            return float(response[key])
        else:
            return int(response[key])
    else:
        return None



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
        global survey_response
        survey_response = json.loads(request.body.decode('utf-8'))
        for key in survey_response:
            if survey_response[key] == '-1':
                survey_response[key] = None

        print ( 'None values adjusted' )
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
            sat = int(survey_response['testScores']['SAT_AVG'])

        act = None
        if 'ACTCMMID' in survey_response['testScores']:
            act = int(survey_response['testScores']['ACTCMMID']) 

        dem = None
        if 'demographicType' in survey_response:
            dem = survey_response['demographicType']

        #Applying KNN to find the best colleges for the user
        user_input = { 'HIGHDEG' : 4, 'SAT_AVG' : sat, 'ACTCMMID' : act, 
            'UGDS_WHITE' : get_demographic( dem, 'UGDS_WHITE' ), 'UGDS_BLACK' : get_demographic( dem, 'UGDS_BLACK' ),
            'UGDS_HISP' : get_demographic( dem, 'UGDS_HISP' ), 'UGDS_ASIAN' : get_demographic( dem, 'UGDS_ASIAN' ), 
            'UGDS_AIAN' : get_demographic( dem, 'UGDS_AIAN' ), 'UGDS_NHPI' : get_demographic( dem, 'UGDS_NHPI' ), 
            'UG25ABV' : get_numeric_val(survey_response, 'UG25ABV'), 'PPTUG_EF' : get_numeric_val(survey_response, 'PPTUG_EF'), 
            'INC_PCT_LO' : get_income_range( survey_response['householdIncome'], 'INC_PCT_LO' ),
            'INC_PCT_M1' : get_income_range( survey_response['householdIncome'], 'INC_PCT_M1' ), 
            'INC_PCT_M2' : get_income_range( survey_response['householdIncome'], 'INC_PCT_M2' ),
            'INC_PCT_H1' : get_income_range( survey_response['householdIncome'], 'INC_PCT_H1' ), 
            'INC_PCT_H2' : get_income_range( survey_response['householdIncome'], 'INC_PCT_H2' ),
            'PAR_ED_PCT_1STGEN' : None, 'C150_4' : 1, 'PCIP14' : 1, 'ADM_RATE': float(survey_response['acceptanceRate']), 
            'MD_EARN_WNE_P10': get_numeric_val(survey_response, 'expectedEarnings'), 'RPY_3YR_RT': 1,
            'MD_EARN_WNE_P6':  get_numeric_val(survey_response, 'expectedEarnings'),'RPY_7YR_RT': 1, 'RPY_5YR_RT': 1,
            'SPRING_TAVG': get_numeric_val(survey_response, 'spring'),'SUMMER_TAVG': get_numeric_val(survey_response, 'summer'),
            'FALL_TAVG': get_numeric_val(survey_response, 'fall'), 'WINTER_TAVG': get_numeric_val(survey_response, 'winter')
            }
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
        if ( int ( survey_response['genderExclusive'] ) ) == 1:
            if survey_response['gender'] == 'male':
                men_only = 1
            elif survey_response['gender'] == 'female':
                women_only = 1

        states = []
        if 'region' in survey_response:
            states = get_states_from_regions( survey_response['region'], survey_response['STABBR'] )
        else:
            states.append( survey_response['STABBR'] )

        historic_type = None
        if 'historicType' in survey_response:
            historic_type = survey_response['historicType']

        rel_affil = None
        if 'RELAFFIL' in survey_response:
            rel_affil = religion_map[survey_response['RELAFFIL']]

        # not sure this is what we want, but taking their desired temp and making an min
        # or max range of 5 in either direction
        winter_range = [float ( survey_response['winter'] ) - 5, float ( survey_response['winter'] ) + 5]
        spring_range = [float ( survey_response['spring'] ) - 5, float ( survey_response['spring'] ) + 5]
        summer_range = [float ( survey_response['summer'] ) - 5, float ( survey_response['summer'] ) + 5]
        fall_range = [float ( survey_response['fall'] ) - 5, float ( survey_response['fall'] ) + 5]

        user_filters = { 'ADM_RATE' : [float(survey_response['acceptanceRate']) / 100.0, 1], 
        'UGDS' : get_student_body_size( survey_response['studentBodySize'] ),
        'TUITIONFEE_IN' : tuition_in, 'TUITIONFEE_OUT' : tuition_out, 'STABBR' : states, 
        'MAIN' : get_numeric_val(survey_response, 'MAIN'), 'CONTROL' : get_numeric_val(survey_response, 'CONTROL'),
        'RELAFFIL' : rel_affil, 'DISTANCEONLY' : get_numeric_val(survey_response, 'DISTANCEONLY'), 
        'HBCU': get_historic( historic_type, 'HBCU' ), 'PBI': get_historic( historic_type, 'PBI' ),
        'ANNHI': get_historic( historic_type, 'ANNHI' ), 'HSI': get_historic( historic_type, 'HSI' ), 
        'NANTI': get_historic( historic_type, 'NANTI' ), 'MENONLY': men_only, 'WOMENONLY': women_only, 
        'CIP14BACHL': 1, 'GRAD_DEBT_MDN10YR': [0,survey_response['monthlyLoans']] }

        print(user_input)
        print(user_filters)
        unit_ids = apply_knn(user_input, user_filters)
        print(unit_ids)
        temp_ids = [int(uid) for uid in unit_ids]
        unit_ids = temp_ids

        # for dev testing
        uni_ids = [199193, 139959, 198419, 228778, 217882, 100858, 243744, 171100, 216597, 228875]

        # fill zip using value from survey JSON
        # example below
        return HttpResponse( json.dumps( { 'ids' : unit_ids, 'zip' : int ( survey_response['zipCode'] ) } ) )


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
        user_sort_data = json.loads( request.body.decode( 'utf-8' ) )
        print ( user_sort_data )

        #unit_ids = perform_topsis(  )

        unit_ids = perform_topsis( user_sort_data, survey_response )
        print ( unit_ids )
        #unit_ids = [139959, 228875, 198419, 199193, 228778, 100858, 217882, 243744, 171100, 216597]
        return HttpResponse( json.dumps( { 'ids' : unit_ids } ) )