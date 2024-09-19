import os
import numpy as np
import pandas as pd
import ast
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from SimilarityScores import SimilarityScores
from DataImport import DataImport

#Load in data
animeCopy = DataImport()


#Feature Engineering
#Extract relevant features from the dataset that will be used for recommendation, such as genres, airing dates, episodes, popularity, and members.
#Convert categorical features like genres into a format suitable for analysis (e.g., one-hot encoding or representing them as lists).
features = animeCopy[['uid','genre','members','episodes']] #In the future add episodes as a feature (could present another recommendation based on episodes)

"""
Encode the features of each show into a numerical vector. This can include:
Genres: Multi-hot encoding (WE will use SCIKIT Learn multilabelbinarizer )
Popularity: Normalize the popularity score, members and episodes
"""


# Start encoding the genre column
#genres_str = features['genre'].unique()
genres_lists =  features['genre'].apply(ast.literal_eval)
unique_genres = set(genre for genres_list in genres_lists for genre in genres_list)
mlb = MultiLabelBinarizer(classes=sorted(unique_genres))
genres_encoded = mlb.fit_transform(genres_lists)
genres_df = pd.DataFrame(genres_encoded, columns=mlb.classes_)
genres_df = genres_df.set_index(features.index)
genre_weight = .2
weighted_genre_df = genres_df * genre_weight
features = pd.concat([features,weighted_genre_df],axis = 1)
features = features.drop(['genre'],axis = 1)

#Begin normalizing members and episodes
scaler = MinMaxScaler()
features[["members", "episodes"]] = scaler.fit_transform(features[["members", "episodes"]])


#Take in user input and find row corresponding to that show
#Capture user preferences or input, such as preferred genres or other criteria for recommendations.
#Process the user input and convert it into a format compatible with the similarity calculation.


#UNCOMMENT WHEN GOING TO NEXT STEP
userInput = input("What was your most recently watched anime? (Please spell out the show's full name) ").lower()
userAnime = animeCopy.loc[animeCopy['title'] == userInput]
userAnime = features.loc[features['uid'] == userAnime['uid'].iloc[0]]


"""
Similarity Calculation:
Will be using Cosine Similarity
Calculate the similarity between each pair of items in the dataset using the chosen metric.
"""

top5MostSimilar = SimilarityScores(features,userAnime,5)
for i in top5MostSimilar:
    print(animeCopy.iloc[i]['title'])



#Recommendation Generation
#Based on the user input and the calculated similarities, generate a list of recommended anime titles.
#Rank the recommended titles based on their similarity to the user input and possibly other factors like popularity or member counts.



#Present Recommendations
#Include additional information about each recommended anime, such as genres, airing dates, episodes, popularity, and member counts.




#Evaluation (Way later)
#Evaluate the performance of the recommendation system using metrics such as precision, recall, or user satisfaction.
#Iterate on the recommendation system by fine-tuning parameters, experimenting with different similarity metrics, or incorporating feedback from users.

