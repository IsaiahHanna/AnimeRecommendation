'''
Written By Isaiah Hanna 2024-09-18

Purpose: List all the possible exceptions for easy troubleshooting
'''

#import logging
from typing import Dict,Union

#TODO : Implement a logging system so that I can log all exceptions

#1xxx -> Type of error 
#x111 -> Specific error

exceptionMessage:Dict[int,str] = {
    #1000s errors: Universal Errors that can occur across all functions
    1001: "Unable to open file",

    #DataImport
    #2000's errors: DataImport Errors
    2001: "Unable to retrieve data from api",
    2002: "Unable to generate random numbers"
}

class customException(Exception):
    def __init__(self,error_code:int,message: str) -> Dict[str,Union[str,int]]:
        self.error_code = error_code
        self.message = message
        super().__init__()

        def __str__(self) -> str:
            return f"Exception Type: {type(self).__name__} \nError Code: {self.error_code} \nException Type: {exceptionMessage.get(self.error_code,'')} \nError Custom Message: {self.message}"
        
class DataImportException(customException):
    #Exception for errors that occur during data collection and set up
    def __init__(self, error_code:int,message:str) -> None:
        super().__init__(error_code = error_code,message =message)