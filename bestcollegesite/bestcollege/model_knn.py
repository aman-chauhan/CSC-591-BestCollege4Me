import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pickle
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.neighbors import NearestNeighbors


#Method to standardize data
def standardize_data(df_sc):
  sc = StandardScaler()
  temp = sc.fit_transform(df_sc)
  df_sc[df_sc.columns] = temp
  return sc, df_sc

#Method to apply PCA
def apply_pca(df_pca):
  pca = PCA(n_components=10)
  df_pca = pca.fit_transform(df_pca)
  return pca, df_pca

#Fitting KNN
def apply_knn(user_input={}, user_filters={}):
  df = pd.read_csv("cleaned_data.csv")

  #Temporary input values for now, 
  #can get rid of these once we have an input coming in from the Survey page
  user_input = {'HIGHDEG': 4, 'SAT_AVG': 1500, 'ACTCMMID': 32, 'UGDS_WHITE': 1, 'UGDS_BLACK': 0, 
  'UGDS_HISP': 0, 'UGDS_ASIAN': 0, 'UGDS_AIAN': 0, 'UGDS_NHPI': 0, 'UGDS_2MOR': 0, 'UGDS_NRA': 0, 
  'UGDS_UNKN': 0, 'UG25ABV': 0, 'PPTUG_EF': 0, 'INC_PCT_LO': 0 , 'INC_PCT_M1': 0, 'INC_PCT_M2': 1, 
  'INC_PCT_H1': 0, 'INC_PCT_H2': 0, 'PAR_ED_PCT_1STGEN': 0, 'C150_4': 1, 'PCIP14': 1}

  user_filters = {'ADM_RATE': [0.1,1], 'UGDS': [5000,50000], 'TUITIONFEE_IN': [0,40000], 
                    'TUITIONFEE_OUT': None, 'STABBR': ['NC'], 'MAIN': 1, 'CONTROL': None, 
                    'RELAFFIL': None, 'DISTANCEONLY': 0, 'HBCU': None, 'PBI': 0, 'ANNHI': 0,
                    'HSI': 0, 'NANTI': 0, 'MENONLY': None, 'WOMENONLY': None,
                    'CIP14BACHL': 1, 'GRAD_DEBT_MDN10YR': [0,300]}

  df_knn = df.copy()

  #Filtering the Data Frame on State Values
  states = user_filters["STABBR"]
  if len(states) > 0:
      df_knn = df_knn.loc[df_knn['STABBR'].isin(states)]
  user_filters.pop("STABBR", None)


  #Dropping input keys which are of no concern to the user
  input_keys_to_drop = []
  for key in user_input:
      if user_input[key] == None:
          cols_to_drop.append(key)
          input_keys_to_drop.append(key)
  for key in input_keys_to_drop:
      user_input.pop(key, None)

  #Adding all the columns except the user input to the drop list
  cols_to_drop = [col for col in df_knn.columns if col not in user_input.keys()]

  #Filtering the data further based on user specified filters
  for col,val in user_filters.items():
      if val:
          if isinstance(val, list):
              df_knn = df_knn[df_knn[col].between(val[0], val[1])]
          else:
              df_knn = df_knn.loc[df_knn[col] == val]
      
  #Dropping all the columns in the drop list
  df_knn.drop(cols_to_drop, axis=1, inplace=True)

  #Standardizing the data
  sc, df_knn_sc = standardize_data(df_knn) 

  #Applying PCA to reduce dimensionality
  pca, df_pca = apply_pca(df_knn_sc)

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





