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

#time.sleep(5)

print("Recommended anime for you to watch are: ")
displayAnime(animeCopy,features,userAnime,'predict')

#Recommendation Generatio
#Based on the user input and the calculated similarities, generate a list of recommended anime titles.
#Rank the recommended titles based on their similarity to the user input and possibly other factors like popularity or member counts.



#Present Recommendations
#Include additional information about each recommended anime, such as genres, airing dates, episodes, popularity, and member counts.




#Evaluation (Way later)
#Evaluate the performance of the recommendation system using metrics such as precision, recall, or user satisfaction.
#Iterate on the recommendation system by fine-tuning parameters, experimenting with different similarity metrics, or incorporating feedback from users.

