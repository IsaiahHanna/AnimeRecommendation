'''
Written By Isaiah Hanna 2024-09-18

Purpose: Functions used for UI
'''
from SimilarityScores import SimilarityScores
import re


#Take in user input and find row corresponding to that show
#Capture user preferences or input, such as preferred genres or other criteria for recommendations.
#Process the user input and convert it into a format compatible with the similarity calculation.
def UserInput(originalDf,features):
    for i in range(3):
        userInput = input("\nWhat was your most recently watched anime? (Please spell out the show's full name) \nAnswer: ").lower()
        userAnime = originalDf[originalDf['title']==userInput]
        if userAnime['title'].empty:
            print("No Matches found. Please check spelling. If the name you tried was in english, try the Japanese name or vice versa.")
        else:
            break
        if i == 2:
            print("You have reached the maximum failed attempts. Please run program again.")
            exit()
    userAnime = features.loc[features['uid'] == userAnime['uid'].iloc[0]]
    return userAnime


#Recommendation Generation
#Based on the user input and the calculated similarities, generate a list of recommended anime titles.
#Rank the recommended titles based on their similarity to the user input and possibly other factors like popularity or member counts.
def PrintSimilarAnime(originalDf,features,userAnime):
    top5MostSimilar = SimilarityScores(features,userAnime,5)
    lengths = []
    for i in top5MostSimilar: 
        lengths.append(len(originalDf.iloc[i]["title"]))
    MaxStrLen = max(lengths) + 5
    print("\n{:<{}} {:<15} {:<15} {:<15}\n".format("Name",MaxStrLen,"Genre","Began Airing","Number of Episodes"))

    for i in top5MostSimilar:
        print("{:<{}} {:<15} {:<15} {:<15}".format(originalDf.iloc[i]['title'].title(),MaxStrLen,originalDf.iloc[i]['genre'].split(",")[0][2:-1],originalDf.iloc[i]['aired'].split("to")[0],originalDf.iloc[i]['episodes']))
    print("\n")
    """
    TODO
    Present Recommendations
    Include additional information about each recommended anime, such as genres, airing dates, episodes, popularity, and member counts.
    """
