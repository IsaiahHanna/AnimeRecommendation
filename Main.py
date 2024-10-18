'''
Written By Isaiah Hanna 2024-09-18

Purpose: Main file for running the Recommendation System
'''

import numpy as np
import pandas as pd
import time
from ImportData.DataImport import DataImport
from PredictionCreation.FeatureEncoding import FeatureEncoding
from Display import UserInput, displayAnime
from PredictionCreation.ModelBuilding import prediction,model
from SimilarityScores import SimilarityScores


class Recommendation:
    # Initialize recommendation object with the animes and features dataframes
    def __init__(self,console:bool = False):
        self.console = console
        self.animes = DataImport()
        self.features = FeatureEncoding()
        self.knn,self.scaler = model(self.anime,self.features)
        
    # Method to take in user input and save it to object
    # Return: True if successful, False otherwise
    def input(self) -> bool:
        if  self.animes.empty or  self.features.empty:
            return False
        
        self.userAnime = UserInput(self.animes,self.features)
        return True
        

    # Method to that produces similar anime (uid's) to the user's input
    # Uses cosine_similarity()
    # Input: The number of anime uid's to save to similarIDs
    # Return: True if successful, False otherwise
    def similar(self,numRows:int = 5) -> bool:
        if not self.userAnime:
            return False
        
        self.similarIDs = SimilarityScores(self.features,self.userAnime,numRows)
        if len(self.similarIDs) == numRows:
            return True
        else: #Change this to raise an error?
            return False
    
        
    # Method to that produces predictions (uid's) for what the user should watch next
    # Uses KNeighborsClassifier with metric = 'cosine' to predict similar anime that the user might like based on their input
    # Input: The number of anime uid's to save to predictions
    # Return: True if successful, False otherwise
    def predict(self,numRows):
        if self.userAnime.empty or not self.knn:
            return False
        
        self.predictions = prediction(self.animes,self.userAnime,numRows)
        if len(self.predictions) == numRows:
            return True
        else: #Change this to raise an error?
            return False
        
    # Method that prints the desired function's output in a readable format for the user
    # Uses KNeighborsClassifier with metric = 'cosine' to predict similar anime that the user might like based on their input
    # Input: The number of anime uid's to save to predictions
    # Return: True if successful, False otherwise   
    @staticmethod
    def display(self,function:str) -> None:
        if self.userAnime.empty or function not in ['predict','similar']:
            return False
        
        displayAnime(self.animes,self.features,self.userAnime,function)
        return True




def ConsoleRecomendation():
    #Load in data
    animeCopy = DataImport()

    #Extract relevant features and encode
    features = FeatureEncoding(animeCopy)


    userAnime = UserInput(animeCopy,features)

    print("Anime similar to your input are: ")
    displayAnime(animeCopy,features,userAnime,'similar')

    #Uncomment line below if the program is running too fast for user to read similar anime
    #time.sleep(5)

    print("Recommended anime for you to watch are: ")
#If you ever plan to use the model instead of the similarity function, please address the issue with the display anime function
#Issue: it has been changed to suit the similarityScore function that outputs the uid's but predict() still outputs indices
    displayAnime(animeCopy,features,userAnime,'predict')


