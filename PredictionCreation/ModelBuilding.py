'''
Written By Isaiah Hanna 2024-10-05

Purpose: Get recommendation data and train/create KNN model
'''
import os
import sys
import pandas as pd
directory_path = os.path.abspath("C:\\Users\\isaia\\AnimeRecommendation")
sys.path.append(directory_path)
from ImportData.DataImport import RecommendationData

def model():
    recExist = RecommendationData(0.8)
    if not recExist:
        print("Recommendation failed, exiting program.")
        exit()
    return