'''
Written By Isaiah Hanna 2024-09-18

Purpose: Import Data File to main.py
'''
import os
import sys
import pandas as pd
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
    global animeCopy
    animeCopy = animeData.copy()
    animeCopy['titles'] = animeCopy['titles'].apply(lambda x: x.lower().strip())
    animeCopy = animeCopy[~((animeCopy['episodes'] == 'na') | (animeCopy['episodes'] == 1))]

    def estimateEpisodes(aired,idx):
        if 'Present' in aired:
            aired = (abs(int(aired[0:4])-2024)*40)
            return aired
        else: 
            return animeCurrent.iloc[idx,4]
      
    animeCurrent = animeCopy.copy()
    animeCurrent['aired'] = animeCopy['aired'].apply(lambda x: 'Current' if 'Present' in x else x)
    animeFinished = animeCurrent[animeCurrent['aired'] != 'Current']
    animeCurrent = animeCopy[~animeCopy['uid'].isin(animeFinished['uid'])]
    animeFinished  = animeFinished.dropna(subset=['episodes'])
    for idx in range(len(animeCurrent)):
        animeCurrent.iloc[idx,4] = int(estimateEpisodes(animeCurrent.iloc[idx,3],idx))
    animeConcat = pd.concat([animeCurrent,animeFinished]).sort_values('uid')
    #animeCopy = animeConcat.dropna(subset='episodes')
    #print(animeConcat['episodes'].isna().values.any())
    return animeConcat

def DataCompleteCollection():
    os.chdir('C:\\Users\\isaia\\AnimeRecommendation\\ImportData')
    animeIDs = []
    animeDf = {'uid':0,'titles':[],'genre':[],'aired':'','episodes': 0,'members':0,'popularity':0,'ranked':0,'score':0,'url':''}
    animeDf = pd.DataFrame(data = animeDf)
    try:
        with open("anime_cache.json",'r') as file:
            data = json.load(file)
            if not bool(data):
                raise DataImportException(error_code=1001,message="Unable to open anime_cache.json")
            else:
                animeIDs = data['sfw']
                if len(animeIDs) == 0:
                    raise DataImportException(error_code=1001,message="Unable to open anime_cache.json")
        outfile = open("ErrorFile.txt","w")
    except Exception as e:
        print(e)
        exit()
        
    idx = 0
    for id in animeIDs:

        nextAnime = {'uid':0,'titles':[],'genre':[],'aired':'','episodes': 0,'members':0,'popularity':0,'ranked':0,'score':0,'url':''}
        try:
            response = requests.get(URL + "/anime/" + str(id))
            if response.status_code == 400:
                raise DataImportException(error_code="2001",message="Request failed to retrieve data from jikan api.")
            data = response.json()['data']

            #Create row with info for nextAnime
            nextAnime['uid'] = id
            for title in data['titles']:
                nextAnime['titles'].append(title['title'])
            nextAnime['genre'] = []
            for genre in data['genres']:
                nextAnime['genre'].append(genre['name'])
            if "?" in data['aired']['string']:
                nextAnime['aired'] = f"{data['aired']['from'][:10]} - Present"  
            elif data['aired']['to'] == None:
                continue
            else:
                nextAnime['aired'] = f"{data['aired']['from'][:10]} - {data['aired']['to'][:10]}"  
            nextAnime['episodes'] = data['episodes']
            nextAnime['members'] = data['members']
            nextAnime['popularity'] = data['popularity']
            nextAnime['ranked'] = data['rank']
            nextAnime['score'] = data['score']
            nextAnime['url'] = data['url']

            animeDf.loc[idx] = nextAnime
            idx += 1
            print(nextAnime['titles'][0] + " collected :)")
            time.sleep(1)
            


        except Exception as e:
            outfile.write(str(e) + "on uid " + str(id) + "\n")

        #Uncomment out break if testing is needed for one row output
        #break 

    animeDf.to_csv('animes.csv',sep=',',encoding='utf-8',index = 'False')

def CheckMissingAnime() -> bool:
    os.chdir('C:\\Users\\isaia\\AnimeRecommendation\\DataImport')
    animeIDs = pd.DataFrame()
    #movieIDs = pd.read_csv('animeMovies.csv')
    newMoviesIDs = []
    try:
        with open("anime_cache.json",'r') as file:
            data = json.load(file)
            if not bool(data):
                raise DataImportException(error_code=1001,message="Unable to open anime_cache.json")
            else:
                animeDf = pd.read_csv('newAnimes.csv')
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

    newAnimeDf = {'uid':0,'titles':[],'genre':[],'aired':'','episodes': 0,'members':0,'popularity':0,'ranked':0,'score':0,'url':''}
    newAnimeDf = pd.DataFrame(newAnimeDf)

    idx = 0
    for id in animeIDs['uid']:

        nextAnime = {'uid':0,'titles':[],'genre':[],'aired':'','episodes': 0,'members':0,'popularity':0,'ranked':0,'score':0,'url':''}
        try:
            response = requests.get(URL + "/anime/" + str(id))
            if response.status_code == 400:
                raise DataImportException(error_code="2001",message="Request failed to retrieve data from jikan api.")
            data = response.json()['data']

            #Prelimiary check for movies
            if not "TV" == data['type'].lower() or "not yet" in data['Status'].lower(): 
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
            if "?" in data['aired']['string']:
                nextAnime['aired'] = f"{data['aired']['from'][:10]} - Present"  
            elif data['aired']['to'] == None:
                newMoviesIDs.append(id)
                print(f"ID Number: {id}, is a movie and has been sent to moviesID dataframe/series")
                continue
            else:
                nextAnime['aired'] = f"{data['aired']['from'][:10]} - {data['aired']['to'][:10]}"  
            nextAnime['episodes'] = data['episodes']
            nextAnime['members'] = data['members']
            nextAnime['popularity'] = data['popularity']
            nextAnime['ranked'] = data['rank']
            nextAnime['score'] = data['score']
            nextAnime['url'] = data['url']

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

    if os.stat("outfile").st_size == 0:
        return True
    else:
        return False

def RecommendationData(percent:float = 1):
    os.chdir('C:\\Users\\isaia\\AnimeRecommendation\\ImportData')
    outfile = open("ErrorFile.txt","a")
    outfile.write("\n\n Beginning the gathering of Recommendation data.\n")
    trainingData = pd.DataFrame({'uid':0,'recommendations':[]})
    randomIDs = []

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
            randomIDs = random.sample(sorted(animeDf['uid']),numAnime)
            if len(randomIDs) == 0:
                raise DataImportException(error_code=2002,message="Unable to generate list containing random uids")
        except Exception as e:
            outfile.write(f"Error:{e}. Attempt to get random IDs failed.")
    else:
        randomIDs = animeDf['uid']
    idx = 0
    for id in randomIDs:
        nextAnime = {'uid': id,'recommendations':[],'recIDs':[]}

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
                continue
            trainingData.loc[idx] = nextAnime
            idx += 1
            print(f"On index {idx}: {nextAnime['uid']} added to training data with recommendation {nextAnime['recommendations'][0]}")
            time.sleep(1)
        
        except Exception as e:
            print(f"Error on index: {idx}.  Error Message: {e}.")
            outfile.write(f"Error Message: {e}. ID Number: {id}.")

    trainingData.to_csv(f'recommendations_{date.today()}.csv',header=False,index=False,mode = 'a') #TODO: Move away from csv and lean into just returning the dataframe itself
    return True #animeDf[animeDf['uid'].isin(randomIDs)] #Return true for function successful and the dataframe containing the random anime and their recommendations


def mergeRecommendationNames():
    df = pd.read_csv(os.getcwd()+"\\\ImportData\\recommendationsOriginal.csv")
    animedf = pd.read_csv(os.getcwd()+"\\\ImportData\\animes.csv")
    df['recommendations'] = df['recommendations'].apply(lambda x: x.strip('[]').split(',')[0])
    animedf['titles'] = animedf['titles'].apply(lambda x: x.strip('[]').split(',')[0])
    animes = {'recId':animedf['uid'],'recommendations':animedf['titles']}
    animesdf = pd.DataFrame(animes)
    mergedDf = pd.merge(animesdf,df,on = 'recommendations')
    print(mergedDf.tail(20))
    mergedDf.to_csv('recommendationsAltered.csv',index=False)
    return

RecommendationData()