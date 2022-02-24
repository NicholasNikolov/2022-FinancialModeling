# import requests
#
# headers = {
#   "apikey": "2d3e1b70-8887-11ec-9541-fdb5a8979f9d"}
#
# params = (
#    ("keyword[]", "AAPL"),
#    ("hl","en"),
# );
#
# response = requests.get('https://app.zenserp.com/api/v1/trends', headers=headers, params=params);

#%%
from pytrends.request import TrendReq
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
#%%
pytrends = TrendReq(hl='en-US', tz=360)

kw_list = ["AAPL"]  # list of keywords to get data

pytrends.build_payload(kw_list, cat= 784, geo = '' , timeframe='now 7-d')

# 1 Interest over Time
data = pytrends.interest_over_time()
data = data.reset_index()

# Testing plots
data = data[data["isPartial"] == False]
#data['date'] = pd.to_datetime(data['date'])
data = data[['date',kw_list[0]]]
data.set_index('date',inplace = True)

#%%
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data)


#X = data.index
#X = np.reshape(X , (-1,1))

index = range(len(data_scaled))
index = np.reshape(index , (-1,1))

#%%
reg = LinearRegression().fit(index, data_scaled)
print(reg.coef_)
#%%
plt.plot(data_scaled)