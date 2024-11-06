'''
Written By Isaiah Hanna 2024-10-05

Purpose: Get recommendation data and train/create KNN model
'''
import os
import sys
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

def model(animeDf,features):
    trainingData = features.set_index('uid')
    knn = NearestNeighbors(
        metric= 'cosine'
        # algorithm = 'auto'
        # n_neighbors
    )
    knn.fit(trainingData)
    return knn

def prediction(df,features,userAnime,knn,numRows):
    if not knn:
        print("KNN model failed to be instantiated. Exiting...")
        exit()
    elif userAnime.empty:
        print("User's input failed to be read. Exiting...")
        exit()
    
    #Find nearest neighbors of user's input
    #userAnime = userAnime[features.columns.tolist()]
    #userScaled = scaler.transform(userAnime)
    indices = knn.kneighbors(userAnime.set_index('uid'),n_neighbors= 6,return_distance=False)  #Returns the distance and indices of the nearest neighbors (default is based on the k used in model's constructor)
    recs = features['uid'].iloc[indices.flatten()].tolist()
    return recs

