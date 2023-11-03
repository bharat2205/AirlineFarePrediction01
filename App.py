from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd
from Source.prediction.predictionPipline import CustomData
from Source.preproMethods.dataReadingAndCleaning import dataReadingAndCleaningClass
from Source.prediction.predictionPipline import PredictPipeline

app = Flask(__name__)

@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")

@app.route("/predict", methods=["GET", "POST"])
@cross_origin()
def predict():
    if request.method=="GET":
        return render_template(home.html)
    else:

        '''dataReadingAndCleaningC = dataReadingAndCleaningClass()
        print(Date_of_Journey, Dep_Time, Arrival_Time)
        Date_of_Journey,Dep_Time,Arrival_Time = dataReadingAndCleaningC.changeDatatypeOfColumn(
            Date_of_Journey = ,Dep_Time = ,Arrival_Time = )'''


        data = CustomData(Airline = request.form.get('Airline'),
                          Date_of_Journey = request.form.get('Dep_Time'),
                          Source = request.form.get('Source'),
                          Destination = request.form.get('Destination'),
                          Dep_Time = request.form.get('Dep_Time'),
                          Arrival_Time = request.form.get('Arrival_Time'),
                          Duration = request.form.get('Duration'),
                          Total_Stops = request.form.get('Total_Stops')
        )

        pred_df = data.getDataAsDataFrame()
        pred_df = data.changeDatatypeOfColumn(pred_df)
        pred_df = data.convertDateInToDayMonthYear(pred_df)

        dataReadingAndCleaningC=dataReadingAndCleaningClass()
        pred_df = dataReadingAndCleaningC.convertHoursAndMinutesToIndependantColumns(df=pred_df, columName="Dep_Time")
        pred_df = dataReadingAndCleaningC.convertHoursAndMinutesToIndependantColumns(df=pred_df, columName="Arrival_Time")
        pred_df = data.isertValueInDuration(pred_df)
        pred_df = dataReadingAndCleaningC.convertDurationToMunutes(pred_df)
        pred_df  = data.dropUncessaryColumns(pred_df)
        PredictPipeline1 = PredictPipeline()
        output = PredictPipeline1.predict(pred_df)


        return render_template('home.html', prediction_text="Your Flight price is Rs. {}".format(output))

    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
