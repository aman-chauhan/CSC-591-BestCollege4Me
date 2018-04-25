from skcriteria import Data, MIN, MAX
from skcriteria.madm import closeness, simple
import pandas as pd
import numpy as np
import os, json, requests

def get_bar_data( lat, lon ):
	google_places_base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?radius=2500&types=bar&location='
	google_places_api_key = '&key=AIzaSyAnsbjT7Dm9Qz9Daf8EgmaL1jaovBfV_Hc'
	google_places_url = google_places_base_url
	google_places_url = google_places_url + str ( lat ) + ','
	google_places_url = google_places_url + str( lon )
	res = requests.get( google_places_url + google_places_api_key ).json()
	
	total = 0
	valid_count = 0
	for i in range( 0, len( res['results'] ) ):
		if 'rating' in res['results'][i]:
			total = total + res['results'][i]['rating']
			valid_count = valid_count + 1

	return ( len( res['results'] ) / 20.0 + ( total / valid_count ) / 5.0 ) / 2.0

def perform_topsis( raw_data, survey_data ):
	SITE_ROOT = os.path.dirname( os.path.realpath(__file__) )
	df = pd.read_csv( SITE_ROOT + "/data/cleaned_data.csv" )
	matrix = []
	ids = []
	# for matrix:
	# overall weather diff avg | crimerate | nightlife score 
	for school in raw_data['schools']:
		cur_id = school['id']
		ids.append( cur_id )
		winter_temp = float( df.loc[df['UNITID'] == np.int64( int ( cur_id ) ), 'WINTER_TAVG'].iloc[0] )
		spring_temp = float( df.loc[df['UNITID'] == np.int64( int ( cur_id ) ), 'SPRING_TAVG'].iloc[0] )
		summer_temp = float( df.loc[df['UNITID'] == np.int64( int ( cur_id ) ), 'SUMMER_TAVG'].iloc[0] )
		fall_temp = float( df.loc[df['UNITID'] == np.int64( int ( cur_id ) ), 'FALL_TAVG'].iloc[0] )

		winter_diff = abs( float( survey_data['winter'] ) - winter_temp )
		spring_diff = abs( float( survey_data['spring'] ) - spring_temp )
		summer_diff = abs( float( survey_data['summer'] ) - summer_temp )
		fall_diff = abs( float( survey_data['fall'] ) - fall_temp )
		diff = ( winter_diff + spring_diff + summer_diff + fall_diff ) / 4.0

		max_crimerate = float( df['CRIME_COUNT'].max() )
		crimerate = float( df.loc[df['UNITID'] == np.int64( int ( cur_id ) ), 'CRIME_COUNT'].iloc[0] )

		matrix.append( [diff, crimerate / max_crimerate, get_bar_data( school['lat'], school['lon'] )] )

	#print ( matrix )
	criteria = [MIN, MIN, MAX]
	data = Data( matrix, criteria,
            weights=[float( raw_data['weather']['importance'] ), float( raw_data['crime']['importance'] ), float( raw_data['nightlife']['importance'] )],
            anames=ids,
            cnames=["weather", "crime", "nightlife"] )

	analysis = closeness.TOPSIS()
	res = analysis.decide( data )
	#print( res )
	rank_list = res.rank_.tolist()
	sorted_ids = [None] * len( ids )
	for i in range( 0, len( rank_list ) ):
		sorted_ids[rank_list[i] - 1] = int ( ids[i] )
	#print( sorted_ids )
	return sorted_ids