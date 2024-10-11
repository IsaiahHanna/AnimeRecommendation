'''
Written By Isaiah Hanna 2024-09-18

Purpose: Main file for running the Recommendation System
'''

import numpy as np
import pandas as pd
import time
from ImportData.DataImport import DataImport
from PredictionCreation.FeatureEncoding import FeatureEncoding
from Display import UserInput, displayAnime
from PredictionCreation.ModelBuilding import prediction
from SimilarityScores import SimilarityScores

#Load in data
animeCopy = DataImport()

#Extract relevant features and encode
features = FeatureEncoding(animeCopy)


userAnime = UserInput(animeCopy,features)

print("Anime similar to your input are: ")
displayAnime(animeCopy,features,userAnime,'similar')

#Uncomment line below if the program is running too fast for user to read similar anime
#time.sleep(5)

print("Recommended anime for you to watch are: ")
displayAnime(animeCopy,features,userAnime,'predict')

