import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pickle
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.neighbors import NearestNeighbors
from .diversity_mix import get_diversity_mix

#Method to standardize data
def standardize_data(df_sc):
  sc = StandardScaler()
  temp = sc.fit_transform(df_sc)
  df_sc[df_sc.columns] = temp
  return sc, df_sc

#Method to apply PCA
def apply_pca(df_pca, n):
  pca = PCA(n_components=n)
  df_pca = pca.fit_transform(df_pca)
  return pca, df_pca

#Fitting KNN
def apply_knn(user_input={}, user_filters={}):
  SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
  df = pd.read_csv(SITE_ROOT+"/data/cleaned_data.csv")

  importance = {'HIGHDEG': 8, 'SAT_AVG': 1, 'ACTCMMID': 1, 'UGDS_WHITE': 4, 'UGDS_BLACK': 4, 
                'UGDS_HISP': 4, 'UGDS_ASIAN': 4, 'UGDS_AIAN': 4, 'UGDS_NHPI': 4, 'UGDS_2MOR': 4, 
                'UGDS_NRA': 4, 'UGDS_UNKN': 4, 'UG25ABV': 3, 'PPTUG_EF': 4, 'INC_PCT_LO': 3 , 
                'INC_PCT_M1': 3, 'INC_PCT_M2': 3, 'INC_PCT_H1': 3, 'INC_PCT_H2': 3, 
                'PAR_ED_PCT_1STGEN': 4, 'C150_4': 1, 'PCIP14': 1, 'RPY_7YR_RT': 1, 
                'RPY_3YR_RT': 1, 'RPY_5YR_RT': 1, "MD_EARN_WNE_P6":1, "MD_EARN_WNE_P10":1, 
                'ADM_RATE': 1, 'COSTT4_A':1 , 'SPRING_TAVG': 2, 'SUMMER_TAVG': 2, 'FALL_TAVG': 2,
                'WINTER_TAVG': 2}

  df_knn = df.copy()

  #Filtering the Data Frame on State Values
  states = user_filters["STABBR"]
  if len(states) > 0:
      df_knn = df_knn.loc[df_knn['STABBR'].isin(states)]
  user_filters.pop("STABBR", None)

  #Adding all the columns except the user input to the drop list
  cols_to_drop = [col for col in df_knn.columns if col not in user_input.keys()]

  #Dropping input keys which are of no concern to the user
  input_keys_to_drop = []
  for key in user_input:
      if user_input[key] == None:
          cols_to_drop.append(key)
          input_keys_to_drop.append(key)
  for key in input_keys_to_drop:
      user_input.pop(key, None)

 

  #Filtering the data further based on user specified filters
  for col,val in user_filters.items():
      if val:
          if isinstance(val, list):
              df_knn = df_knn[df_knn[col].between(val[0], val[1])]
          else:
              df_knn = df_knn.loc[df_knn[col] == val]
      
  #Dropping all the columns in the drop list
  df_knn.drop(cols_to_drop, axis=1, inplace=True)

  #returning if not enough colleges left upon filtering
  if df_knn.shape[0] < 1:
    return []

  #Standardizing the data
  sc, df_knn_sc = standardize_data(df_knn) 

  #Assigning weights to features for a weighted KNN
  for col in list(df_knn_sc.columns):
    df_knn_sc[col] = df_knn_sc[col].apply(lambda x: x*importance[col])

  #Applying PCA to reduce dimensionality
  comps = 10
  if df_knn_sc.shape[1] < 10:
    comps = df_knn_sc.shape[1]
  pca, df_pca = apply_pca(df_knn_sc, comps)

  #Putting the User input into a data frame
  df_input = pd.DataFrame(data=None, columns=df_knn_sc.columns)
  df_input = df_input.append(user_input, ignore_index=True)

  #Standardizing the user input
  temp1 = sc.transform(df_input)
  df_input[df_input.columns] = temp1

  #Checking if at least 10 rows are there in the dataset,
  #if not reducing the number of final results
  n = 10
  if df_knn_sc.shape[0] < 10:
      n = df_knn_sc.shape[0]

  #Fitting Nearest Neighbors on the dataset 
  nbrs = NearestNeighbors(n_neighbors=n, algorithm='kd_tree').fit(df_pca)
  distances, indices = nbrs.kneighbors(pca.transform(df_input))
  
  #Returning the UNITIDs of the resulting universities/colleges
  df_result = df_knn_sc.iloc[indices[0]]
  return list(df.iloc[list(df_result.index)].UNITID)





