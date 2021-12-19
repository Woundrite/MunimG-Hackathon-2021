import joblib
import pandas as pd
import numpy as np
from tensorflow import keras

model = keras.models.load_model("stonks_AMZN.h5")
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
test = np.array([1906.58996582], ndmin=3)

finally_prediction = model.predict(test)
print(finally_prediction)

# from matplotlib import pyplot as plt
# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
# import pandas_datareader as web
# import datetime as dt

# from sklearn.preprocessing import MinMaxScaler
#from tensorflow.keras.models import Sequential
#from tensorflow.keras.layers import Dense, Dropout, LSTM

# company = 'AMZN'
# test_start = dt.datetime(2020, 1, 1)
# test_end = dt.datetime.now()
# start = dt.datetime(2012, 1, 1)
# end = dt.datetime(2020, 1, 1)
# data = web.DataReader(company, 'yahoo', start, end)
# scaler = MinMaxScaler(feature_range=(0,1)) 
# test_data = web.DataReader(company, 'yahoo', test_start, test_end)
# actual_prices = test_data['Close'].values

# total_dataset = pd.concat((data['Close'], test_data['Close']), axis=0)

# prediction_days = 60

# model_inputs = total_dataset[len(total_dataset) - len(test_data) - prediction_days:].values
# model_inputs = model_inputs.reshape(-1,1)


# print(model_inputs)
# #print(total_dataset)