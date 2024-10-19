'''
Written By Isaiah Hanna 2024-09-18

Purpose: Import Data File to main.py
'''
import os
import sys
import pandas as pd
import numpy as np
import requests
import json
import re
import time
import random
from datetime import date
directory_path = os.path.abspath("C:\\Users\\isaia\\AnimeRecommendation")
sys.path.append(directory_path)
from ExceptionsList import DataImportException
from ImportData.api_Url import URL



os.chdir('C:\\Users\\isaia\\AnimeRecommendation\\ImportData')


def DataImport(check:bool = False):
    os.chdir('C:\\Users\\isaia\\AnimeRecommendation\\ImportData')
    # Load the dataset
    if check:
        for i in range(4):
            loadAnime = CheckMissingAnime()
            if loadAnime == True:
                break
            elif i == 3:
                exit()
    with open('animes.csv',encoding = 'latin-1') as f:
        animeData = pd.read_csv(f)
    animeCopy = animeData.copy()
    animeCopy['titles'] = animeCopy['titles'].apply(lambda x: x.lower().strip())
    animeCopy = animeCopy[~((animeCopy['episodes'] == 'na') | (animeCopy['episodes'] == 1))]

    def estimateEpisodes(aired,idx):
        if 'Present' in aired:
            episodesEst = (abs(int(aired[0:4])-2024)*40)
            return episodesEst
        elif "Unknown" in aired:
            episodesEst = 10
            return episodesEst
        else: 
            return 10
      
    animeCurrent = animeCopy.loc[animeCopy['episodes'] == np.nan].copy()
    animeCurrent['aired'] = animeCopy['aired'].apply(lambda x: 'Current' if 'Present' in x else x)
    animeFinished = animeCurrent[animeCurrent['aired'] != 'Current']
    animeCurrent = animeCopy[~animeCopy['uid'].isin(animeFinished['uid'])]
    animeFinished  = animeFinished.dropna(subset=['episodes'])
    for idx in range(len(animeCurrent)):
        animeCurrent.iloc[idx,4] = int(estimateEpisodes(animeCurrent.iloc[idx,7],idx))
    animeConcat = pd.concat([animeCurrent,animeFinished]).sort_values('uid')
    for val in ['na',np.nan,pd.NaT]:
        animeConcat['episodes'] = animeConcat['episodes'].replace(val,10)
    #animeCopy = animeConcat.dropna(subset='episodes')
    #print(animeConcat['episodes'].isna().values.any())
    return animeConcat

def DataCompleteCollection():
    os.chdir('C:\\Users\\isaia\\AnimeRecommendation\\ImportData')
    animeIDs = []
    newMoviesIDs = []
    animeDf = {'uid':0,'titles':[],'genre':[],'type':'','themes':[],'demographics':[],'rating':'','aired':'','episodes': 0,'members':0,'popularity':0,'ranked':0,'score':0,'url':'','synopsis':'','studios':[],'licensors':[]}
    animeDf = pd.DataFrame(data = animeDf)
    try:
        with open("anime_cache.json",'r') as file:
            data = json.load(file)
            if not bool(data):
                raise DataImportException(error_code=1001,message="Unable to open anime_cache.json")
            else:
                knownMoviesIDs = pd.read_csv("moviesIDsRedo.csv")
                animeIDs = data['sfw']
                if len(animeIDs) == 0:
                    raise DataImportException(error_code=1001,message="Unable to open anime_cache.json")
        outfile = open("ErrorFile.txt","w")
    except Exception as e:
        print(e)
        exit()

    animeIDs = pd.array(data = animeIDs)
    animeIDs = animeIDs[~ (animeIDs.isin(knownMoviesIDs['id']))]

    idx = 0
    for id in animeIDs:

        nextAnime = {'uid':0,'titles':[],'type':'','genre':[],'themes':[],'demographics':[],'rating':'','aired':'','episodes': 0,'members':0,'popularity':0,'ranked':0,'score':0,'url':'','synopsis':'','studios':[],'licensors':[]}
        try:
            response = requests.get(URL + "/anime/" + str(id))
            if response.status_code == 400:
                raise DataImportException(error_code="2001",message="Request failed to retrieve data from jikan api.")
            data = response.json()['data']

            if data['type'] not in ['ONA','OVA','TV'] or "not yet" in data['status'].lower():
                newMoviesIDs.append(id)
                print(f"ID Number: {id}, is a movie and has been sent to moviesID dataframe/series")
                continue

            #Create row with info for nextAnime
            nextAnime['uid'] = id
            for title in data['titles']:
                nextAnime['titles'].append(title['title'])
            nextAnime['genre'] = []
            for genre in data['genres']:
                nextAnime['genre'].append(genre['name'])
            nextAnime['type'] = data['type']
            if len(data['themes']) != 0:
                for theme in data['themes']:
                    nextAnime['themes'].append(theme['name'])
            else:
                nextAnime['themes'] = np.nan
            if len(data['demographics']) != 0:
                for demo in data['demographics']:
                    nextAnime['demographics'].append(demo['name'])
            else:
                nextAnime['demographics'] = np.nan
            if data['rating'] != '':
                nextAnime['rating'] = data['rating']    
            if "?" in data['aired']['string']:
                nextAnime['aired'] = f"{data['aired']['from'][:10]} - Present"  
            elif data['aired']['to'] == None and data['type'] in ['ONA','OVA','TV']: #Second half is redundant since this is checked earlier
                if data['aired']['from'] == None:
                    nextAnime['aired'] = "Unknown"
                else:
                    f"{data['aired']['from'][:10]} - {data['aired']['from'][:10]}"
            else:
                nextAnime['aired'] = f"{data['aired']['from'][:10]} - {data['aired']['to'][:10]}"  
            nextAnime['episodes'] = data['episodes']
            nextAnime['members'] = data['members']
            nextAnime['popularity'] = data['popularity']
            nextAnime['ranked'] = data['rank']
            nextAnime['score'] = data['score']
            nextAnime['url'] = data['url']
            if data['synopsis'] != '':
                nextAnime['synopsis'] = data['synopsis']
            else: 
                nextAnime['synopsis'] = np.nan
            if len(data['studios']) != 0:
                for studio in data['studios']:
                    nextAnime['studios'].append(studio['name'])
            else:
                nextAnime['studios'] = np.nan
            if len(data['licensors']) != 0:
                for licensor in data['licensors']:
                    nextAnime['licensors'].append(licensor['name'])
            else:
                nextAnime['licensors'] = np.nan


            animeDf.loc[idx] = nextAnime
            idx += 1
            print(nextAnime['titles'][0] + " collected :)")
            time.sleep(1)
            


        except Exception as e:
            outfile.write(str(e) + "on uid " + str(id) + "\n")

        #Uncomment out break if testing is needed for one row output
        #break 

    animeDf.to_csv('animesNew.csv',sep=',',encoding='utf-8',index = False)
    moviesIDS = pd.DataFrame({'id':newMoviesIDs})
    moviesIDS.to_csv('moviesIDsRedo.csv',sep = ',',encoding = 'utf-8',index = False,mode = 'a',header = False)
    outfile.close()
    return



def CheckMissingAnime() -> bool:
    os.chdir('C:\\Users\\isaia\\AnimeRecommendation\\ImportData')
    animeIDs = pd.DataFrame()
    #movieIDs = pd.read_csv('animeMovies.csv')
    newMoviesIDs = []
    try:
        with open("anime_cache.json",'r') as file:
            data = json.load(file)
            if not bool(data):
                raise DataImportException(error_code=1001,message="Unable to open anime_cache.json")
            else:
                animeDf = pd.read_csv('animes.csv')
                knownMovies = pd.read_csv('moviesIDs.csv')
                if animeDf.empty:
                    raise DataImportException(error_code=1001,message="Unable to write animes.csv to dataframe")
                animeIDs = pd.DataFrame({'uid':data['sfw']})
                if len(animeIDs) == 0:
                    raise DataImportException(error_code=1001,message="Unable to open anime_cache.json")
        outfile = open("ErrorFile.txt","w")
    except Exception as e:
        print(e)
        exit()

    animeIDs['uid'] = animeIDs['uid'].astype(str)
    animeDf['uid'] = animeDf['uid'].astype(str)
    knownMovies['id'] = knownMovies['id'].astype(str)
    animeIDs = animeIDs[~ (animeIDs['uid'].isin(animeDf['uid']))]
    animeIDs = animeIDs[~ (animeIDs['uid'].isin(knownMovies['id']))]

    newAnimeDf = {'uid':0,'titles':[],'genre':[],'type':'','themes':[],'demographics':[],'rating':'','aired':'','episodes': 0,'members':0,'popularity':0,'ranked':0,'score':0,'url':'','synopsis':'','studios':[],'licensors':[]}
    newAnimeDf = pd.DataFrame(newAnimeDf)

    idx = 0
    for id in animeIDs['uid']:

        nextAnime = {'uid':0,'titles':[],'genre':[],'type':'','themes':[],'demographics':[],'rating':'','aired':'','episodes': 0,'members':0,'popularity':0,'ranked':0,'score':0,'url':'','synopsis':'','studios':[],'licensors':[]}
        try:
            response = requests.get(URL + "/anime/" + str(id))
            if response.status_code == 400:
                raise DataImportException(error_code="2001",message="Request failed to retrieve data from jikan api.")
            data = response.json()['data']

            #Prelimiary check for movies
            if data['type'] not in ['ONA','OVA','TV'] or "not yet" in data['status'].lower(): 
                newMoviesIDs.append(id)
                print(f"ID Number: {id}, is a movie and has been sent to moviesID dataframe/series")
                continue

            #Create row with info for nextAnime
            nextAnime['uid'] = id
            for title in data['titles']:
                nextAnime['titles'].append(title['title'])
            nextAnime['genre'] = []
            for genre in data['genres']:
                nextAnime['genre'].append(genre['name'])
            if len(data['themes']) != 0:
                for theme in data['themes']:
                    nextAnime['themes'].append(theme['name'])
            else:
                nextAnime['themes'] = np.nan
            if len(data['demographics']) != 0:
                for demo in data['demographics']:
                    nextAnime['demographics'].append(demo['name'])
            else:
                nextAnime['demographics'] = np.nan
            if data['rating'] != '':
                nextAnime['rating'] = data['rating']    
            if "?" in data['aired']['string']:
                nextAnime['aired'] = f"{data['aired']['from'][:10]} - Present"  
            elif data['aired']['to'] == None and data['type'] in ['ONA','OVA','TV']: #Second half is redundant since this is checked earlier
                if data['aired']['from'] == None:
                    nextAnime['aired'] = "Unknown"
                else:
                    f"{data['aired']['from'][:10]} - {data['aired']['from'][:10]}"
            else:
                nextAnime['aired'] = f"{data['aired']['from'][:10]} - {data['aired']['to'][:10]}"  
            nextAnime['episodes'] = data['episodes']
            nextAnime['members'] = data['members']
            nextAnime['popularity'] = data['popularity']
            nextAnime['ranked'] = data['rank']
            nextAnime['score'] = data['score']
            nextAnime['url'] = data['url']
            if data['synopsis'] != '':
                nextAnime['synopsis'] = data['synopsis']
            else: 
                nextAnime['synopsis'] = np.nan
            if len(data['studios']) != 0:
                for studio in data['studios']:
                    nextAnime['studios'].append(studio['name'])
            else:
                nextAnime['studios'] = np.nan
            if len(data['licensors']) != 0:
                for licensor in data['licensors']:
                    nextAnime['licensors'].append(licensor['name'])
            else:
                nextAnime['licensors'] = np.nan

            newAnimeDf.loc[idx] = nextAnime
            idx += 1
            print(nextAnime['titles'][0] + " collected :)")
            time.sleep(1)
            


        except Exception as e:
            outfile.write(f"Error Message: {e}. ID Number: {id}. Index Number: {idx}. \n")

        #Uncomment out break if testing is needed for one row output
        #break 

    newAnimeDf.to_csv('animes.csv',sep=',',encoding='utf-8',index = False,mode = 'a',header = False)
    moviesIDS = pd.DataFrame({'id':newMoviesIDs})
    moviesIDS.to_csv('moviesIDs.csv',sep = ',',encoding = 'utf-8',index = False,mode = 'a',header = False)

    outfile.close()

    if os.stat("ErrorFile.txt").st_size == 0:
        return True
    else:
        return False

def RecommendationData(percent:float = 1,complete:bool = False):
    os.chdir('C:\\Users\\isaia\\AnimeRecommendation\\ImportData')
    outfile = open("ErrorFile.txt","w")
    outfile.write("\n\n Beginning the gathering of Recommendation data.\n")
    trainingData = pd.DataFrame({'uid':0,'recommendations':[],'recIDs':[]})
    IDList = []

    #Import animeDf
    try:
        animeDf = pd.read_csv('animes.csv')
        if animeDf.empty:
            raise DataImportException(error_code=1001,message="Unable to write animes.csv to dataframe")
    except Exception as e:
        print(f"Error: {e}. Unable to write animes.csv to dataframe, aborting RecommendationData function.")
        return False,animeDf
    
    #Generate random entries to be used as training data
    if percent != 1:
        try:
            numAnime = int(animeDf.shape[0] * percent)
            #random.seed()
            IDList = random.sample(sorted(animeDf['uid']),numAnime)
            if len(IDList) == 0:
                raise DataImportException(error_code=2002,message="Unable to generate list containing random uids")
        except Exception as e:
            outfile.write(f"Error:{e}. Attempt to get random IDs failed.")
    else:
        IDList = animeDf['uid']
    if not complete:
        animeFinished = pd.read_csv("recommendations.csv")
        animeUnfinished = animeDf[~ (animeDf['uid'].isin(animeFinished['uid']))]
        IDList = animeUnfinished['uid']
    idx = 0
    attempts = 0
    for id in IDList:
        nextAnime = {'uid': id,'recommendations':[],'recIDs':[]}
        attempts += 1

        try:
            response = requests.get(f"https://api.jikan.moe/v4/anime/{id}/recommendations")
            if response.status_code == 400:
                raise DataImportException(error_code="2001",message="Request failed to retrieve data from jikan api.")
            data = response.json()['data']

            nextAnime['uid'] = id
            if len(data) != 0:
                for entry in data:
                    nextAnime['recommendations'].append(entry['entry']['title'])
                    nextAnime['recIDs'].append(entry['entry']['mal_id'])
            else:
                 nextAnime['recommendations'] = np.nan
                 nextAnime['recIDs'] = np.nan
                 print(f"On index {idx}: {nextAnime['uid']} added to training data with no recommendations")
            trainingData.loc[idx] = nextAnime
            print(f"On index {idx}: {nextAnime['uid']} added to training data with recommendation {nextAnime['recommendations']}")
            idx += 1
            successRate = idx/attempts
            print(f"Success Rate: {successRate}")
            print(f"Recommendation Empty Ratio {trainingData.dropna(subset='recommendations',inplace=False).shape[0]}/{attempts}")
            print(f"ID Empty Ratio {trainingData.dropna(subset='recIDs',inplace=False).shape[0]}/{attempts}")
            if successRate < 0.9:
                print(f"Success rate has dropped below suitable levels on record {idx}. Exiting...")
                exit()
            time.sleep(1)
        
        except Exception as e:
            print(f"Error on index: {idx}.  Error Message: {e}.")
            outfile.write(f"Error Message: {e}. ID Number: {id}.")
    
    if complete:
        trainingData.to_csv(f'recommendations_{date.today()}.csv',header=True,index=False,mode = 'w') #TODO: Move away from csv and lean into just returning the dataframe itself
    if not complete:
        trainingData.to_csv(f'recommendations_{date.today()}.csv',header=False,index=False,mode = 'a')
    outfile.close()

    if os.stat("ErrorFile.txt").st_size == 0:
        return True
    else:
        return False #animeDf[animeDf['uid'].isin(randomIDs)] #Return true for function successful and the dataframe containing the random anime and their recommendations


#Takes a recommendations file that is missing RecIDs and adds the ID for all the recommendation
def mergeRecommendation(merge:str):
    if os.getcwd() != 'C:\\Users\\isaia\\AnimeRecommendation\\ImportData':
        os.chdir('C:\\Users\\isaia\\AnimeRecommendation\\ImportData')
    df = pd.read_csv("recommendationsOriginal.csv")
    animedf = pd.read_csv("animes.csv")
    if merge.lower() == 'name':
        df['recommendations'] = df['recommendations'].apply(lambda x: x.strip('[]').split(',')[0])
        animedf['titles'] = animedf['titles'].apply(lambda x: x.strip('[]').split(',')[0])
        animes = {'recId':animedf['uid'],'recommendations':animedf['titles']}
        animesdf = pd.DataFrame(animes)
        mergedDf = pd.merge(animesdf,df,on = 'recommendations')  
        mergedDf.to_csv('recommendationsAltered.csv',index=False)

    if merge.lower() == 'id':
        df['RecommendationsID'] = df['RecommendationsID'].apply(lambda x: [])
        for idx,row in df.iterrows(): #Loop over each row in the recommendations set
            for rec in df.iloc[idx,1].strip('[]').split(','):
                rec = rec.strip("'")
                recID = animedf[animedf['titles'].apply(lambda x: x.strip('[]').split(',')[0]) == rec] #Check for which anime's first title matches the recommendation
                df.iloc[idx,2].append(recID)
            print(f"On Index:{idx}, {len(df.iloc[idx,2])} recommendation ids were added.")
        df.to_csv('recommendationsAltered.csv',index=False)
    return

# while True:
#     finished = CheckMissingAnime()
#     if finished:
#         print("ALL FINISHED SUCCESSFULLY")
#         exit()
#     else:
#         continue