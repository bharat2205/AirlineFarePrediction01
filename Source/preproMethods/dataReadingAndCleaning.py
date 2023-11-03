
from ExceptionLoggerAndUtils.exception import CustomException
from ExceptionLoggerAndUtils.logger import App_Logger
from datetime import datetime

import pandas as pd
import os
import sys
import json

class dataReadingAndCleaningClass():
    """ This class shall be used for handling all the SQL operations.
        Written By: Shivraj Shinde//Version: 1.0//Revisions: None
    """

    def __init__(self):
        self.File_Path = "C:\\Users\\Admin\\Downloads\\Data_Train.xlsx"
        self.schema_path = 'Schemas/schema_data.json'
        self.folder_path = "cleanedData/"

        self.log_writer = App_Logger()
        self.cwd=os.getcwd()
        self.file_object = open(self.cwd+'preprocessing.txt', 'a+')

    def readingDataSet(self):
        try:
            #print(self.FilePath)
            self.log_writer.log(self.file_object, 'Start of Validation on files for Training')
            self.df = pd.read_excel(self.File_Path,engine='openpyxl')
            return self.df
        except Exception as e:
            raise CustomException(e,sys)
    def removeNullValues(self,df):
        try:
            routeMissingRow = df[df['Route'].isnull() == True].index
            df.drop(routeMissingRow, inplace=True)
            return df
        except Exception as e:
            raise CustomException(e,sys)



    def removingUnevenValues(self,df):
        try:
            df['Destination'].replace(to_replace="New Delhi", value="Delhi", inplace=True)
            return df
        except Exception as e:
            raise CustomException(e,sys)

    def removingOutlier(self,column_names,airlineName,df):
        """ Written By  : Shivraj Shinde//Version: 1.0//Revisions: None
            Description : This method removes all the outlir from the data.
            Output      : Return Final_data data with no outlier
            On Failure  : Raise Exception
        """
        try:
            final_df = pd.DataFrame(columns=column_names)

            for key, value in airlineName.items():
                airDataSet = ""
                airDataSet = df[df['Airline'] == key]
                q1 = airDataSet['Price'].quantile(value[0])
                q3 = airDataSet['Price'].quantile(value[1])
                IQR = q3 - q1
                lowerLimit = q1 - IQR * 1.5
                upperLimit = q3 + IQR * 1.5
                lowerLimitIndex = list(airDataSet[airDataSet['Price'] <= lowerLimit].index)
                upperLimitIndex = list(airDataSet[airDataSet['Price'] >= upperLimit].index)

                value = int(airDataSet.shape[0])
                if value > 5:
                    airDataSet.drop(lowerLimitIndex, axis=0, inplace=True)
                    airDataSet.drop(upperLimitIndex, axis=0, inplace=True)
                else:
                    pass
                final_df = pd.concat([final_df, airDataSet],axis=0)  # axis=0 is the default and means appending vertically

            final_df = final_df.sort_index(ascending=True)
            return final_df

        except Exception as e:
            raise CustomException(e,sys)

    def convertDateInToDayMonthYear(self,df):
        """ Written By  : Shivraj Shinde//Version: 1.0//Revisions: None
            Description : This will create three different columns Day,Month,Year.
            Output      : Return dataFrame with independant Column as Day,Month,Year Columns
            On Failure  : Raise Exception
        """
        try:
            df['Day'] = pd.to_datetime(df["Date_of_Journey"], format="%d/%m/%Y").dt.day
            df['Month'] = pd.to_datetime(df['Date_of_Journey'], format="%d/%m/%Y").dt.month
            df['Year'] = pd.to_datetime(df['Date_of_Journey'], format="%d/%m/%Y").dt.year

            return df

        except Exception as e:
            raise CustomException(e,sys)

    def convertHoursAndMinutesToIndependantColumns(self,df,columName):
        """ Written By  : Shivraj Shinde//Version: 1.0//Revisions: None
            Description : This will create two idependant columns Hours and Minites.
            Output      : Return dataFrame with independant Hours and Minites.
            On Failure  : Raise Exception
        """

        try:
            columName1 = columName.split("_")[0]
            df[columName1 + "_Hours"] = pd.to_datetime(df[columName]).dt.hour
            df[columName1 + "_Minutes"] = pd.to_datetime(df[columName]).dt.minute

            return df

        except Exception as e:
            raise CustomException(e,sys)

    def convertDurationToMunutes(self,df):
        try:
            df["hoursMinutes"] = 0

            for i in df.index:
                if " " in df.loc[i, 'Duration']:
                    column1 = df.loc[i, 'Duration'].split(" ")[0]
                    column2 = df.loc[i, 'Duration'].split(" ")[1]
                    if "h" in column1:
                        column1 = (int(column1.replace("h", "")) * 60)
                    elif "m" in column1:
                        column1 = (int(column1.replace("m", "")))
                    if "h" in column2:
                        column2 = (int(column2.replace("h", "")) * 60)
                    elif "m" in column2:
                        column2 = (int(column2.replace("m", "")))

                    df.loc[i, 'hoursMinutes'] = column1 + column2
                else:
                    column1 = df.loc[i, 'Duration']
                    if "h" in column1:
                        column1 = (int(column1.replace("h", "")) * 60)
                    elif "m" in column1:
                        column1 = (int(column1.replace("m", "")))
                    df.loc[i, 'hoursMinutes'] = column1
            return df

        except Exception as e:
            raise CustomException(e, sys)

    def saveDataToFolder(self,df):
        try:
            if not os.path.exists(self.folder_path):
                os.makedirs(self.folder_path)
            file_name = "cleanedDataFile.csv"  # Name of the CSV file
            file_path = os.path.join(self.folder_path, file_name)  # Full file path
            df.to_csv(file_path, index=False)  # Save the DataFrame as a CSV file
            print(f"CSV file saved to {file_path}")

        except Exception as e:
            raise CustomException(e, sys)

    def dropUncessaryColumns(self,df):
        try:
            df = df.drop(["Arrival_Time","Dep_Time","Date_of_Journey","Route","Duration","Additional_Info"], axis = 1)
            return df
        except Exception as e:
            raise CustomException(e, sys)

    def valuesFromSchema(self):

        """ Method Name : valuesFromSchema
            Written By  : Shivraj Shinde//Version: 1.0//Revisions: None
            Description : This method extracts all the relevant information from the pre-defined "Schema" file.
            Output      : LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, Number of Columns
            On Failure  : Raise Exception
        """
        try:
            with open(self.schema_path, 'r') as f:
                dic = json.load(f)
                f.close()
            column_names = dic['ColName']
            airlineName = dic['airlineName']

            NumberofColumns = dic['NumberofColumns']

            self.log_writer.log(self.file_object,"schema Reading Completed")
            return  column_names, NumberofColumns, airlineName

        except Exception as e:
            raise CustomException(e, sys)

