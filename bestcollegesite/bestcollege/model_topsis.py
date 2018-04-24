from skcriteria import Data, MIN, MAX
from skcriteria.madm import closeness, simple
import pandas as pd
import numpy as np
import os

def perform_topsis( raw_data, survey_data ):
	SITE_ROOT = os.path.dirname( os.path.realpath(__file__) )
	df = pd.read_csv( SITE_ROOT + "/data/cleaned_data.csv" )
	matrix = []
	ids = []
	# for matrix:
	# overall weather diff avg | crimerate | nightlife score 
	for key in raw_data['nightlife']['schools']:
		ids.append( key )
		winter_temp = float( df.loc[df['UNITID'] == np.int64( int ( key ) ), 'WINTER_TAVG'].iloc[0] )
		spring_temp = float( df.loc[df['UNITID'] == np.int64( int ( key ) ), 'SPRING_TAVG'].iloc[0] )
		summer_temp = float( df.loc[df['UNITID'] == np.int64( int ( key ) ), 'SUMMER_TAVG'].iloc[0] )
		fall_temp = float( df.loc[df['UNITID'] == np.int64( int ( key ) ), 'FALL_TAVG'].iloc[0] )

		winter_diff = abs( float( survey_data['winter'] ) - winter_temp )
		spring_diff = abs( float( survey_data['spring'] ) - spring_temp )
		summer_diff = abs( float( survey_data['summer'] ) - summer_temp )
		fall_diff = abs( float( survey_data['fall'] ) - fall_temp )
		diff = ( winter_diff + spring_diff + summer_diff + fall_diff ) / 4.0

		crimerate = float( df.loc[df['UNITID'] == np.int64( int ( key ) ), 'CRIME_COUNT'].iloc[0] )

		matrix.append( [diff, crimerate, float( raw_data['nightlife']['schools'][key]['nightlife_score'] )] )

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