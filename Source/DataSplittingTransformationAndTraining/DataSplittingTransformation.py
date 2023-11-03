from ExceptionLoggerAndUtils.exception import CustomException
from ExceptionLoggerAndUtils.logger import App_Logger
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline,Pipeline
from sklearn.preprocessing import OneHotEncoder,OrdinalEncoder
from sklearn.preprocessing import MinMaxScaler,StandardScaler
import os
import sys
import pandas as pd

class dataSplittingTransformationClass():

    def dataReadingAndSplitting(self,path):
        try:
            final_df = pd.read_csv(path)
            print(final_df)
            y = final_df.loc[:, 'Price']
            X = final_df.drop(['Price'], axis=1)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=355)
            return (X_train, X_test, y_train, y_test)

        except Exception as e:
            raise CustomException(e, sys)

    def dataTransformation(self):
        try:
            trf1 = ColumnTransformer([
                ('OneHot', OneHotEncoder(drop='first', handle_unknown='error'), ['Airline','Source','Destination'])], remainder='passthrough')
            trf2 = ColumnTransformer([
                ('Ordinal', OrdinalEncoder(categories=[['non-stop', '1 stop', '2 stops', '3 stops', '4 stops']]), [19])]
                , remainder='passthrough')

            trf3 = ColumnTransformer([
                ('scale', StandardScaler(), slice(0, 25))
            ])

            pipe = make_pipeline(trf1,trf2,trf3)


            return pipe

        except Exception as e:
            raise CustomException(e, sys)




