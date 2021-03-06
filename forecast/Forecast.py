from keras.models import Sequential
from tensorflow.keras.models import load_model
from keras.layers import Dense
from keras.callbacks import EarlyStopping

import numpy as np
import tensorflow as tf
import pandas as pd

#########################################################################
#  Load DNN Model
#########################################################################
def load_model_except():
    m = input("Enter Model Name : ");

    try:
        Weather_Forecast_Mode_Local = load_model(m);
    except:
        print("Load Fail\n");
        Weather_Forecast_Mode_Local = -1;

    return Weather_Forecast_Mode_Local;

Weather_Forecast_Model = load_model_except();

while(Weather_Forecast_Model == -1):
    Weather_Forecast_Model = load_model_except();

# Show Model Summary
Weather_Forecast_Model.summary();

print("\n\nLoad Model\n\n");

#########################################################################
#  Load Current Weather Data
#########################################################################
def load_Data_except():
    local = input("Input Current Weather Data : ");

    try:
        X_data_Local = pd.read_csv(local, names=['기온', '습도', '이슬점', '기압']);
    except:
        print("Load Fail\n");
        X_data_Local = None;

    return X_data_Local;

X_data = load_Data_except();

while(X_data is None):
    X_data = load_Data_except();

print("Load Local Data\n\n");

#########################################################################
#  Get time to predict
#########################################################################

pred_time = input("Predict Time (hour) : ");
pred_time = int(pred_time);

#########################################################################
#  Data Processing
#########################################################################

# 0 Temperature

# 1 Humidity        습도 = 습도 * 0.01
X_data.iloc[0, 1] = X_data.iloc[0, 1] * 0.01;

# 2 Dew Point

# 3 Pressure        기압 = 기압 - 1000
X_data.iloc[0, 3] = (X_data.iloc[0, 3] - 1000);

print("Current Local Weather");
print(X_data);
print("\n\n\n");

#########################################################################
#  Predict
#########################################################################
prediction = Weather_Forecast_Model.predict(X_data);

time = 0;
while(time < pred_time - 1):
    Temp = Weather_Forecast_Model.predict(prediction);
    time = time + 1;

# result data processing
Forecast_Temperature = prediction[0][0];
Forecast_Humidity = prediction[0][1] * 100;
Forecast_Dew_Point = prediction[0][2];
Forecast_Pressure = (prediction[0][3]) + 1000;

#########################################################################
#  Print and Save Result
#########################################################################
print(">>>>>> Weather Forecast <<<<<<\n\n");

print("Local Weather after ", pred_time, " Hour(s)");
print(prediction);
print("\n");

print("기온: ", Forecast_Temperature, "C");
print("습도: ", Forecast_Humidity, "%");
print("이슬점: ", Forecast_Dew_Point, "C");
print("기압: ", Forecast_Pressure, "hpa");

# save
out = input("\n\nSave Prediction >");

Save_Array = [Forecast_Temperature, Forecast_Humidity, Forecast_Dew_Point, Forecast_Pressure];
Save_File = [Save_Array];
Forecast_File = pd.DataFrame(Save_File);
Forecast_File.to_csv(out, header = False, index = False);

print("\n\n SAVE \n");