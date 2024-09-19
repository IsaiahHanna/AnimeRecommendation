'''
Written By Isaiah Hanna 2024-09-18

Purpose: Select Features and Return Encoded df
'''
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
import ast

def FeatureEncoding(animeCopy):
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

    return features
