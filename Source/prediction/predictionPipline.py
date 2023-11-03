import sys
import pandas as pd
from ExceptionLoggerAndUtils.logger import App_Logger
from ExceptionLoggerAndUtils.exception import CustomException
from ExceptionLoggerAndUtils.utils import load_object

class PredictPipeline():
    def __init__(self):
        pass

    def predict(self,features):
        try:
            modelPath = "artifacts/model.pkl"
            preprocessorPath = "artifacts/transformation.pkl"
            model = load_object(file_path=modelPath)
            transformation = load_object(file_path=preprocessorPath)
            dataScaled = transformation.transform(features)
            pred = model.predict(dataScaled)
            return pred
        except Exception as e:
            raise CustomException(e, sys)



class CustomData():
        def __init__(self,Airline:str,Date_of_Journey:str,Source:str,Destination:str,
                     Dep_Time:str,Arrival_Time:str,Duration:str,Total_Stops:str):
            self.Airline = Airline
            self.Date_of_Journey = Date_of_Journey
            self.Source = Source
            self.Destination = Destination
            self.Dep_Time = Dep_Time
            self.Arrival_Time = Arrival_Time
            self.Duration = Duration
            self.Total_Stops = Total_Stops

        def getDataAsDataFrame(self):
            inputDict = {
                "Airline": [self.Airline],
                "Date_of_Journey": [self.Date_of_Journey],
                "Source": [self.Source],
                "Destination": [self.Destination],
                "Dep_Time": [self.Dep_Time],
                "Arrival_Time": [self.Arrival_Time],
                "Duration": [self.Duration],
                "Total_Stops": [self.Total_Stops]

            }

            return pd.DataFrame(inputDict)

        def changeDatatypeOfColumn(self,pred_df):
            date_format = "%Y-%m-%d %H:%M:%S"
            pred_df['Date_of_Journey'] = pd.to_datetime(pred_df['Date_of_Journey'], format=date_format)
            pred_df['Dep_Time'] = pd.to_datetime(pred_df['Dep_Time'], format=date_format)
            pred_df['Arrival_Time'] = pd.to_datetime(pred_df['Arrival_Time'], format=date_format)

            return pred_df

        def convertDateInToDayMonthYear(self, df):
            """ Written By  : Shivraj Shinde//Version: 1.0//Revisions: None
                Description : This will create three different columns Day,Month,Year.
                Output      : Return dataFrame with independant Column as Day,Month,Year Columns
                On Failure  : Raise Exception
            """
            try:
                df['Day'] = pd.to_datetime(df["Date_of_Journey"], format="%Y-%m-%d").dt.day
                df['Month'] = pd.to_datetime(df['Date_of_Journey'], format="%Y-%m-%d").dt.month
                df['Year'] = pd.to_datetime(df['Date_of_Journey'], format="%Y-%m-%d").dt.year

                return df

            except Exception as e:
                raise CustomException(e, sys)

        def isertValueInDuration(self, pred_df):
            pred_df['Duration'] = pred_df['Arrival_Time'] - pred_df['Dep_Time']
            #hours = str()
            Hours = pd.to_datetime(pred_df['Duration']).dt.hour
            Minutes = pd.to_datetime(pred_df['Duration']).dt.minute
            print(Hours)
            print(Hours)

            pred_df['Duration'] = pred_df['Duration'].astype(str)

            pred_df['Duration'] = str(Hours[0])+"h "+str(Minutes[0])+"m"

            #minutes =str(pd.to_datetime(pred_df['Duration']).dt.minute + "m ")
            #pred_df['Duration'] =hours +"h "+minutes + "m "


            return pred_df

        def dropUncessaryColumns(self,df):
            try:
                df = df.drop(["Arrival_Time","Dep_Time","Date_of_Journey","Duration"], axis = 1)
                return df
            except Exception as e:
                raise CustomException(e, sys)
