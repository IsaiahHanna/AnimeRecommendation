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

def ConsoleRecomendation():
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
#If you ever plan to use the model instead of the similarity function, please address the issue with the display anime function
#Issue: it has been changed to suit the similarityScore function that outputs the uid's but predict() still outputs indices
    displayAnime(animeCopy,features,userAnime,'predict')



# def webRecommendation(show: str) -> str:
#     #Load in data
#     animeCopy = DataImport()

#     #Extract relevant features and encode
#     features = FeatureEncoding(animeCopy)

#     userAnime = UserInput(animeCopy,features,show,console = False)

#     similarAnime = SimilarityScores(features,userAnime,3)  #Bring in the 3 indices of the 3 most similar anime to the user's input
#     recIDX = similarAnime[1]

#     return animeCopy.iloc[recIDX,1].strip("[]").split(",")[0].title() #Return the primary title for the most similar anime to the user's input
