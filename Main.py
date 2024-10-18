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
        self.features = FeatureEncoding(self.animes)
        self.knn,self.scaler = model(self.animes,self.features)
        
    # Method to take in user input and save it to object
    # Return: True if successful, False otherwise
    def input(self,show:str = 'naruto') -> bool:
        if  self.animes.empty or  self.features.empty:
            return False
        
        if self.console:
            self.userAnime = UserInput(self.animes,self.features,console = self.console)
            return True
        if not self.console:
            self.userAnime = UserInput(self.animes,self.features,show,self.console)
            return True
        

    # Method to that produces similar anime (uid's) to the user's input
    # Uses cosine_similarity()
    # Input: The number of anime uid's to save to similarIDs
    # Return: True if successful, False otherwise
    def similar(self,numRows:int = 5) -> bool:
        if  self.userAnime.empty:
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
    def predict(self,numRows:int = 5):
        if self.userAnime.empty or not self.knn:
            return False
        
        self.predictions = prediction(self.animes,self.features,self.userAnime,self.knn,self.scaler,numRows)
        if len(self.predictions) == numRows:
            return True
        else: #Change this to raise an error?
            return False
        
    # Method that prints the desired function's output in a readable format for the user
    # Uses KNeighborsClassifier with metric = 'cosine' to predict similar anime that the user might like based on their input
    # Input: The number of anime uid's to save to predictions
    # Return: True if successful, False otherwise   
    def display(self,function:str) -> None:
        if self.userAnime.empty or function not in ['predict','similar']:
            return False
        
        if function == 'predict':
            displayAnime(self.animes,self.features,self.userAnime,self.predictions)
            return True
        if function == 'similar':
            displayAnime(self.animes,self.features,self.userAnime,self.similarIDs)
            return True



def consoleUse():
    console = Recommendation(console =  True)
    console.input()
    console.predict()
    console.similar()
    console.display(function ='similar')
    console.display(function = 'predict')
    
#consoleUse()



