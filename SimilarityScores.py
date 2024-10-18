'''
Written By Isaiah Hanna 2024-09-18

Purpose: Similarity Scores Function
'''
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

"""
Similarity Calculation:
Will be using Cosine Similarity
Calculate the similarity between each pair of items in the dataset using the chosen metric.
"""

#Input: features dataframe, UserAnime series (1 row dataframe) and number of Similar anime to produce  
#Output: An array with the indices of the most similar anime to the user's input
def SimilarityScores(features,target,numRows): 
    features = features.drop(index = features.index[features['uid'] == target.iloc[0,0]].tolist(),axis = 0) # Features dataframe without the target row
    target = np.array(target)
    features = np.array(features)
    cosine_sim = cosine_similarity(features[:,1:],target[:,1:]).reshape(1, -1)[0] #Pass all columns except for uid into the cosine_similarity function
    similarEntriesIdx = cosine_sim.argsort()[::-1][:numRows+1] 
    similarEntries = []
    for idx in similarEntriesIdx:
        similarEntries.append(features[idx,0])
    return similarEntries