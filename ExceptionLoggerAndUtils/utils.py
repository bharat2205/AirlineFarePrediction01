import os
import sys
import numpy as np
from sklearn import metrics
from sklearn.metrics import mean_squared_error, mean_absolute_error
import warnings

import pandas as pd
#import dill
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV,RandomizedSearchCV

from ExceptionLoggerAndUtils.exception import CustomException


def save_object(file_path, obj):
    try:

        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)


def evaluate_Regression_models(X_train, y_train, X_test, y_test, models, param):
    try:

        modelScore = {'modelName'   :[],
                      'R2core'      :[],
                      'aR2'         :[],
                      'MSE'         :[],
                      'MAE'         :[],
                      'RMSE'        :[]
                      }

        ar2Score = {}

        j = 0
        k = 0
        print(j)

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning)  # Ignore the UserWarning

            for i in range(len(list(models))):
                print(j)
                j = j + 1
                model = list(models.values())[i]

                print(list(models.keys())[i])

                para = param[list(models.keys())[i]]
                print(para)

                gs = RandomizedSearchCV(model, para)
                gs.fit(X_train, y_train)

                model.set_params(**gs.best_params_)

                model.fit(X_train, y_train)

                y_train_pred = model.predict(X_train)

                y_test_pred = model.predict(X_test)

                R2train_model_score = r2_score(y_train, y_train_pred)
                R2test_model_score = r2_score(y_test, y_test_pred)

                aR2 = 1 - (1 - R2test_model_score) * (len(y_test) - 1) / (len(y_test) - X_test.shape[1] - 1)

                MSE = metrics.mean_squared_error(y_test, y_test_pred)
                MAE = metrics.mean_absolute_error(y_test, y_test_pred)
                RMSE = np.sqrt(metrics.mean_squared_error(y_test, y_test_pred))

                ar2Score[list(models.keys())[i]] = aR2

                modelName = list(models.keys())[i]

                modelScore['modelName'].append(modelName)
                modelScore['R2core'].append(R2test_model_score)
                modelScore['aR2'].append(aR2)
                modelScore['MSE'].append(MSE)
                modelScore['MAE'].append(MAE)
                modelScore['RMSE'].append(RMSE)
                k = k+1

        print(pd.DataFrame(modelScore))
        #print(modelScore)
        print(ar2Score)

        return ar2Score

    except Exception as e:
        raise CustomException(e, sys)


def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)


