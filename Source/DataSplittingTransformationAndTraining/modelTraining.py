import os
import sys
from dataclasses import dataclass

from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.svm import SVR

from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from ExceptionLoggerAndUtils.logger import App_Logger
from ExceptionLoggerAndUtils.exception import CustomException
#from xgboost import XGBRegressor

from ExceptionLoggerAndUtils.utils import save_object, evaluate_Regression_models


class ModelTrainerClass:
    def __init__(self):
        self.log_writer = App_Logger()
        self.trained_model_file_path = os.path.join("artifacts", "model.pkl")

    def modelsToTrainAndParameters(self):
        try:
            models = {
                "Linear Regression"     : LinearRegression(),
                "lasso"                 : Lasso(),

            }

            params = {
                    "Linear Regression": {
                        #'alpha': [0.01, 0.1, 1.0, 10.0],  # Regularization strength (alpha)
                        'fit_intercept': [True, False]  # Whether to fit the intercept
                    },
                    "lasso": {
                        'alpha': [0.01, 0.1, 1.0, 10.0],  # Regularization strength (alpha)
                        'fit_intercept': [True, False]  # Whether to fit the intercept
                    },

                    }

            return models , params
        except Exception as e:
            raise CustomException(e, sys)


    def modelTraingMethod(self,X_train, X_test, y_train, y_test,models,params):
        try:

            model_report: dict = evaluate_Regression_models(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test,
                                                 models=models, param=params)

            ## below returns the best model score from dict
            best_model_score = max(sorted(model_report.values()))


            ## below returns the best model Name score from dict
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]

            ## To get best model name from dict
            best_model = models[best_model_name]

            print("Best found model on both training and testing dataset")
            print(best_model)

            save_object(
                file_path=self.trained_model_file_path,
                obj=best_model
            )

            predicted = best_model.predict(X_test)

            r2_square = r2_score(y_test, predicted)
            return r2_square

        except Exception as e:
            raise CustomException(e, sys)
