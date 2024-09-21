'''
Written By Isaiah Hanna 2024-09-18

Purpose: Import Data File to main.py
'''
import os
import pandas as pd

os.chdir('C:\\Users\\isaia\\AnimeRecommendation')

def DataImport():
    # Load the dataset
    with open('animes.csv',encoding = 'latin-1') as f:
        animeData = pd.read_csv(f)
    animeCopy = animeData.copy()
    animeCopy['title'] = animeCopy['title'].str.lower().str.strip()
    animeCopy = animeCopy[~((animeCopy['episodes'] == 'na') | (animeCopy['episodes'] == 1))]
    animeCopy  = animeCopy.dropna(subset=['episodes'])
    return animeCopy