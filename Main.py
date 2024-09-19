'''
Written By Isaiah Hanna 2024-09-18

Purpose: Main file for running the Recommendation System
'''

import numpy as np
import pandas as pd
from DataImport import DataImport
from FeatureEncoding import FeatureEncoding
from Display import UserInput, PrintSimilarAnime

#Load in data
animeCopy = DataImport()

#Extract relevant features and encode
features = FeatureEncoding(animeCopy)


userAnime = UserInput(animeCopy,features)

PrintSimilarAnime(animeCopy,features,userAnime)



#Recommendation Generation
#Based on the user input and the calculated similarities, generate a list of recommended anime titles.
#Rank the recommended titles based on their similarity to the user input and possibly other factors like popularity or member counts.



#Present Recommendations
#Include additional information about each recommended anime, such as genres, airing dates, episodes, popularity, and member counts.




#Evaluation (Way later)
#Evaluate the performance of the recommendation system using metrics such as precision, recall, or user satisfaction.
#Iterate on the recommendation system by fine-tuning parameters, experimenting with different similarity metrics, or incorporating feedback from users.

