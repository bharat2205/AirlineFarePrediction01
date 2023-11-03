from ExceptionLoggerAndUtils.exception import CustomException
from ExceptionLoggerAndUtils.logger import App_Logger
from Source.preproMethods.dataReadingAndCleaning import dataReadingAndCleaningClass
import os
import sys
import pandas as pd

class preproInitiator():
    def __init__(self):
        self.log_writer = App_Logger()
        self.cleaningObj = dataReadingAndCleaningClass()
        self.cwd=os.getcwd()
        self.file_object = open(self.cwd+'preprocessing.txt', 'a+')

    def preprocessingOfData(self):
        try:
            self.log_writer.log(self.file_object, "Good_Data folder deleted!!!")
            column_names, NumberofColumns, airlineName = self.cleaningObj.valuesFromSchema()


            df = self.cleaningObj.readingDataSet()
            df = self.cleaningObj.removeNullValues(df)
            df = self.cleaningObj.removingUnevenValues(df)
            df = self.cleaningObj.removingOutlier(column_names,airlineName,df)
            df = self.cleaningObj.convertDateInToDayMonthYear(df)
            df = self.cleaningObj.convertHoursAndMinutesToIndependantColumns(df=df,columName="Dep_Time")
            df = self.cleaningObj.convertHoursAndMinutesToIndependantColumns(df=df,columName="Arrival_Time")
            df = self.cleaningObj.convertDurationToMunutes(df)
            df = self.cleaningObj.dropUncessaryColumns(df)
            self.cleaningObj.saveDataToFolder(df)
            print(df.columns)
            return df

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    preproInitiatorObj = preproInitiator()
    preproInitiatorObj.preprocessingOfData()
