# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 19:48:30 2022

@author: nikol
"""

from pytrends.request import TrendReq
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np


def trend_analytics(ticker):
    print("Running src.trend_analytics.trend_analytics")
    '''
    '''
    
    data = run_query([ticker])
    
    data = preprocess_trend_data(data , ticker)
    
    data_scaled = scale_data(data)
    
    index = build_index(data_scaled)
    
    trend_score = compute_trend(index , data_scaled)
    
    return trend_score
    
    
def run_query(ticker_list):
    print("Running src.trend_analytics.run_query")
    '''
    Formulate the trends query and query for data for the specific ticker being
    studied. The method will run for business news (documentation included) and
    will look back over the last week. 
    
    Parameters:
    ticker_list (list) : Just the single ticker being studied but provided as
            a list since that is the format expected.
            
    Returns:
    data (DataFrame) : Returns the full Pandas DataFrame including the isPartial
            field which indicates whether or not the full time period is populated.
    '''
    
    # Build the pytrend Trend Request for TimeZone CST (which is 360)
    pytrends = TrendReq(hl='en-US', tz=360)
    
    # Build the trend query payload. Restrict to business news.
    # Ref: https://github.com/pat310/google-trends-api/wiki/Google-Trends-Categories
    pytrends.build_payload(ticker_list, cat= 784, geo = '' , timeframe='now 7-d')

    # Form the data return
    data = pytrends.interest_over_time()
    
    return data


def preprocess_trend_data(data , ticker):
    print("Running src.trend_analytics.preprocess_trend_data")
    '''
    Preprocess (but do not scale) the data. This will remove the isPartial field
    
    Parameters:
    data (DataFrame) : The Pandas DataFrame with isPartial included.
    
    ticker (str) : The ticker symbol being studied.
    
    Returns:
    data (DataFrame) : The DataFrame with the isPartial field removed.
    '''
    
    # Only include fully completed dates
    data = data[data["isPartial"] == False]
    
    # Restrict to only include the ticker data.
    data = data[[ticker]]
    
    return data


def scale_data(data):
    print("Running trend_analytics.scale_data")
    '''
    Scale the data using the MinMaxScaler() to scale data to the set of 
    real numbers [0,1] in R. When computing the trend_score I hope to allow for
    the freedom to do comparisons between datasets (if the need arises).
    
    Parameters:
    data (DataFrame) : the DataFrame to be scaled.
    
    Returns:
    data_scaled (nparray) : The array with scaled data.
    '''
    
    scaler = MinMaxScaler()
    
    data_scaled = scaler.fit_transform(data)

    index = range(len(data_scaled))
    index = np.reshape(index , (-1,1))
    
    return data_scaled
    
def build_index(data):
    print("Running src.trend_analytics.build_index")
    '''
    Create an index (just a range of values) from 0 to the length of data.
    This will be used as the X axis when fitting a simple regressor.
    
    Parameters:
    data (nparray) : Should be the scaled nparray from scale_data().
    
    Returns:
    index (nparray) : The index array reshaped for use in LinearRegression().
    '''
    
    index = range(len(data))
    index = np.reshape(index , (-1,1))

    return index


def compute_trend(X , y):
    print("Running src.trend_analysis.compute_trend")
    '''
    Computes a trend score which should, theoretically, be standardized across
    time series. May prove useful for future studies. This is a simple regressor
    fit on data for searches of the particular ticker every 2 hours for 7 days.
    
    The trend score is a simple linear regressor fit to this data. 
    
    The goal here is to identify growth or decay in the interst in a particular
    stock. This should not be used as a sole predictor. There is a possibility for
    mid-period increases in stock searches (e.g., growth in interest then decay)
    which would yield a near 0 trend score. But this is still interesting to study
    in the event that some insight can be derived.
    
    Parameters:
    X (nparray) : The index along the X-axis for building the regressor.
    
    y (nparray) : The scaled data along the y-axis for building the regressor.
    
    Returns:
    trend_score (float) : The trend score. Not rounded.
    '''
    
    reg = LinearRegression().fit(X , y)
    
    trend_score = reg.coef_
    
    trend_score = float(trend_score)
    
    return trend_score


if __name__ == '__main__':
    trend = trend_analytics("AAPL")
    








