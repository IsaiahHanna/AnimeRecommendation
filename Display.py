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
def UserInput(originalDf,features,show_name: str = 'naruto' ,console: bool = True):
    for i in range(3):
        if console == True:
            userInput = input("\nWhat was your most recently watched anime? (Please spell out the show's full name) \nAnswer: ").lower()
        elif console == False:
            userInput = f"'{show_name.lower()}'"
            mask = originalDf.copy()
            mask['titles'] = mask['titles'].apply(lambda x: True if userInput in x.strip("[]").split(",") else False)
            mask.sort_values(by='titles',inplace = True,ascending = False)
            userAnime = originalDf.loc[originalDf['uid'] == mask.iloc[0,0]]
            userAnime = features.loc[features['uid'] == userAnime['uid'].iloc[0]]
            return userAnime


        mask = originalDf.copy()
        mask['titles'] = mask['titles'].apply(lambda x: userInput in x)
        mask.sort_values(by='titles',inplace = True,ascending = False)
        possibleTargets = mask.loc[mask['titles'] == True]


        if len(possibleTargets) > 1:
            if console == True:
                targetMapping = {}
                print("There are multiple anime that contain that name. \nOptions: ")
                for i in range(len(possibleTargets)):
                    targetMapping[i] = possibleTargets.iloc[i,0]
                    uid = int(possibleTargets.iloc[i,0])
                    print(f"{i}. {originalDf.loc[originalDf['uid'] == uid].iloc[0,1].strip('[]').split(',')[0]}")
                target = input("Please select the number for which anime you intended to be used as input: ")
                target = targetMapping[int(target)]
                userAnime = originalDf.loc[originalDf['uid'] == int(target)]
                break

            #Code below is to be used if auto-complete dropdown is ever removed
            #This will require asking the user which option and then recovering that input and running it through this function again
            # elif console ==False and attempt == 2:
            #     possibleTitles = []
            #     for i in range(len(possibleTargets)):
            #         uid = int(possibleTargets.iloc[i,0])
            #         possibleTitles.append(originalDf.loc[originalDf['uid'] == uid].iloc[0,1].strip('[]').split(',')[0])
            #     return possibleTitles


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
    return userAnime #Note that userAnime is a one row pd.Dataframe


"""
    DISPLAY FUNCTIONS
    -----------------
    TODO
    Present Recommendations
    Include additional information about each recommended anime, such as genres, airing dates, episodes, popularity, and member counts.
    """

def displayAnime(originalDf,features,userAnime,topAnime):
    titles = []
    lengths = []
    for i in range(len(topAnime)):
        id = topAnime[i]
        titles.append(originalDf.loc[originalDf['uid'] == id]["titles"].iloc[0].strip('[]').split(',')[0])
        lengths.append(len(titles[i]))
    MaxStrLen = max(lengths) + 5
    print("\n{:<{}} {:<15} {:<15} {:<15}\n".format("Name",MaxStrLen,"Genre","Began Airing","Number of Episodes"))

    for i in range(len(topAnime)):
        id = topAnime[i]
        print("{:<{}} {:<15} {:<15} {:<15}".format(titles[i].title(),MaxStrLen,originalDf.loc[originalDf['uid'] == id]['genre'].iloc[0].split(",")[0][2:-1],originalDf.loc[originalDf['uid'] == id]['aired'].iloc[0].split("-")[0],originalDf.loc[originalDf['uid'] == id]['episodes'].iloc[0]))
    print("\n")
    
