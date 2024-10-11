'''
Written By Isaiah Hanna 2024-09-18

Purpose: Functions used for UI
'''
from SimilarityScores import SimilarityScores
from PredictionCreation.ModelBuilding import prediction
import re


#Take in user input and find row corresponding to that show
#Capture user preferences or input, such as preferred genres or other criteria for recommendations.
#Process the user input and convert it into a format compatible with the similarity calculation.
def UserInput(originalDf,features):
    for i in range(3):
        userInput = input("\nWhat was your most recently watched anime? (Please spell out the show's full name) \nAnswer: ").lower()
        mask = originalDf.copy()
        mask['titles'] = mask['titles'].apply(lambda x: userInput in x)
        mask.sort_values(by='titles',inplace = True,ascending = False)
        possibleTargets = mask.loc[mask['titles'] == True]
        if len(possibleTargets) > 1:
            print("There are multiple anime that contain that name. \nOptions: ")
            for i in range(len(possibleTargets)):
                uid = int(possibleTargets.iloc[i,0])
                print(f"{i}. {originalDf.loc[originalDf['uid'] == uid].iloc[0,1].strip('[]').split(',')[0]}")
            target = input("Please select the number for which anime you intended to be used as input: ")
            target = possibleTargets.iloc[i,0]
            userAnime = originalDf.loc[originalDf['uid'] == int(target)]
            break
        elif len(possibleTargets) == 1:
            target = possibleTargets.iloc[0,0]
            userAnime = originalDf.loc[originalDf['uid'] == int(target)]
            break
        elif possibleTargets.empty:
            print("No Matches found. Please check spelling. If the name you tried was in english, try the Japanese name or vice versa.")
        if i == 2:
            print("You have reached the maximum failed attempts. Please run program again.")
            exit()
    userAnime = features.loc[features['uid'] == userAnime['uid'].iloc[0]]
    return userAnime


"""
    DISPLAY FUNCTIONS
    -----------------
    TODO
    Present Recommendations
    Include additional information about each recommended anime, such as genres, airing dates, episodes, popularity, and member counts.
    """

def displayAnime(originalDf,features,userAnime,function):
    titles = []
    if function.lower() == 'similar':
        topAnime = SimilarityScores(features,userAnime,5)
    elif function.lower() == 'predict':
        target = userAnime 
        topAnime = prediction(originalDf,target,5)[0]
    lengths = []
    for i in range(len(topAnime)):
        idx = topAnime[i]
        titles.append(originalDf.iloc[idx]["titles"].strip('[]').split(',')[0])
        lengths.append(len(titles[i]))
    MaxStrLen = max(lengths) + 5
    print("\n{:<{}} {:<15} {:<15} {:<15}\n".format("Name",MaxStrLen,"Genre","Began Airing","Number of Episodes"))

    for i in range(len(topAnime)):
        idx = topAnime[i]
        print("{:<{}} {:<15} {:<15} {:<15}".format(titles[i].title(),MaxStrLen,originalDf.iloc[idx]['genre'].split(",")[0][:],originalDf.iloc[idx]['aired'].split("-")[0],originalDf.iloc[idx]['episodes']))
    print("\n")
    """
    TODO
    Present Recommendations
    Include additional information about each recommended anime, such as genres, airing dates, episodes, popularity, and member counts.
    """
