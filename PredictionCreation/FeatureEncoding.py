'''
Written By Isaiah Hanna 2024-09-18

Purpose: Select Features and Return Encoded df
'''
import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
import ast

def FeatureEncoding(animeCopy):
    #Feature Engineering
    #Extract relevant features from the dataset that will be used for recommendation, such as genres, airing dates, episodes, popularity, and members.
    #Convert categorical features like genres into a format suitable for analysis (e.g., one-hot encoding or representing them as lists).

    features = animeCopy[['uid','genre','type','themes','demographics','rating','members','studios','licensors']] #In the future add episodes and/or aired?

    """
    Encode the features of each show into a numerical vector. This can include:
    Genres: Multi-hot encoding (WE will use SCIKIT Learn multilabelbinarizer )
    Popularity: Normalize the members 
    """


    # Start encoding the columns that contain lists
    listFeatures = ['genre','themes','demographics','studios','licensors']
    stringFeatures = ['type','rating']

    # Loop that will perform the encoding for each list-feature
    for feature in listFeatures:
        entry_lists =  features[feature].apply(ast.literal_eval)
        unique_entries = set(entry for entry_list in entry_lists for entry in entry_list)
        mlb = MultiLabelBinarizer(classes=sorted(unique_entries))
        features_encoded = mlb.fit_transform(entry_lists)
        features_df = pd.DataFrame(features_encoded, columns=mlb.classes_)
        features_df = features_df.set_index(features.index)
        features = pd.concat([features,features_df],axis = 1)
        features = features.drop([feature],axis = 1)

    #Loop that will perform the encoding for each string-feature
    for feature in stringFeatures:
        unique_entries = set(feature for feature in features[feature])
        mlb = MultiLabelBinarizer(classes = sorted(unique_entries))
        features_encoded =  mlb.fit_transform(features[feature])
        features_df = pd.DataFrame(features_encoded,columns=mlb.classes_)
        features_df = features_df.set_index(features.index)
        features = pd.concat([features,features_df],axis = 1)
        features = features.drop([feature],axis = 1)


    return features
