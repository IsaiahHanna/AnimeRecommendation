'''
Written By Isaiah Hanna 2024-09-18

Purpose: Similarity Scores Function
'''
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

def SimilarityScores(features,target,numRows): 
    target = np.array(target)
    features = np.array(features)

    cosine_sim = cosine_similarity(features,target).reshape(1, -1)[0]
    similarEntries = cosine_sim.argsort()[::-1][:numRows]
    return similarEntries