'''
Written By Isaiah Hanna 2024-09-18

Purpose: Functions used for UI
'''
from SimilarityScores import SimilarityScores

def UserInput(originalDf,features):
    #Take in user input and find row corresponding to that show
    #Capture user preferences or input, such as preferred genres or other criteria for recommendations.
    #Process the user input and convert it into a format compatible with the similarity calculation.

    userInput = input("What was your most recently watched anime? (Please spell out the show's full name) ").lower()
    userAnime = originalDf.loc[originalDf['title'] == userInput]
    userAnime = features.loc[features['uid'] == userAnime['uid'].iloc[0]]
    return userAnime

def PrintSimilarAnime(originalDf,features,userAnime):
    top5MostSimilar = SimilarityScores(features,userAnime,5)
    for i in top5MostSimilar:
        print(originalDf.iloc[i]['title'])
