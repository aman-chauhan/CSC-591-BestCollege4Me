from sklearn.neighbors import NearestNeighbors
from pprint import pprint
import pandas as pd
import numpy as np
import json
import os


def get_diversity_mix(home_state, option):
    SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
    df = pd.read_csv(SITE_ROOT+"/data/cleaned_data.csv", low_memory=False)
    df = df[['UNITID', 'INSTNM', 'ZIP', 'CITY', 'STABBR', 'UGDS_WHITE', 'UGDS_BLACK',
             'UGDS_HISP', 'UGDS_ASIAN', 'UGDS_AIAN', 'UGDS_NHPI', 'UGDS_UNKN']]
    X = df[['UNITID', 'INSTNM', 'ZIP', 'CITY', 'STABBR']]
    Y = df[['UGDS_WHITE', 'UGDS_BLACK', 'UGDS_HISP', 'UGDS_ASIAN', 'UGDS_AIAN', 'UGDS_NHPI', 'UGDS_UNKN']]
    homestates = json.load(open(SITE_ROOT+'/data/homestates.json'))
    oy = Y[X['STABBR'] != home_state]
    nbrs = NearestNeighbors(n_neighbors=len(homestates), algorithm='brute', metric='l1').fit(oy.values)
    d, i = nbrs.kneighbors(np.asarray(homestates[home_state]).reshape((1, -1)))
    if option == 1:
        return homestates[home_state]
    elif option == 2:
        return Y.values[i[0]][:10].mean(axis=0).tolist()
    else:
        return Y.values[i[0]][-10:].mean(axis=0).tolist()
