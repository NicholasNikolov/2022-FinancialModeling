# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 14:05:53 2022
@author: Nicholas Nikolov

These methods perform the data processing to prepare the data for modeling.
This includes interpolating nulls, determining datatypes, formatting strings, etc.
"""

import src.db_connection as db
import pandas as pd


def read_format_df(ticker: str):
    print("Running src.data_processing.read_format_df()")
    '''
    Read from the database and format the resultant data into a proper pandas
    DataFrame to support feeding the data into future models.
    
    ~~~ Presently no parameter input is provided. May eventually add
    ~~~ conditional inputs allowing for specific ticker symbols.
    
    Parameters:
    ticker (str) : The ticker symbol for which to build the DataFrame.
    
    Returns:
    full_df (DataFrame) : The Pandas DataFrame containing the extracted data
            from the database.
    '''

    # Establish the DB connection
    db_connect = db.DBMethods()

    # Data query to extract dataset.
    query = "SELECT * FROM yh_finance_db.financial_data where TICKER_SYMBOL = %s;"
    params = [ticker]
    query_result = db_connect.db_read(query, params)

    # Convert to pandas DataFrame.
    full_df = pd.DataFrame(query_result)

    return full_df


def establish_data_types(df):
    print("Running src.data_processing.establish_data_types")
    '''
    Establish the datatypes within the dataframe based on the provided dictionary.
    '''


def establish_floats(df, data_types):
    print("Running src.data_processing.establish_floats")
    '''
    '''


def format_timestamp(df):
    print("Running src.data_processing.format_timestamp")
    '''
    '''
    # Format the datetime.
    df = pd.to_datetime(df['TIME_STAMP'])

    return df


def interpolate_nulls(df):
    print("Running src.data_processing.interpolate_nulls()")
    '''
    Fill missing null values based on the most recent values surrounding the
    null entry. Data interpolation works by taking an average of the value
    immediately preceding the null and the one immediately after. In cases
    of multiple nulls in a row, the interpolater should set all nulls to the
    same average.
    '''


def MARKET_CAP_to_numeric(df):
    print("Running src.data_processing.MARKET_CAP_to_numeric")
    '''
    Format MARKET_CAP properly. It is stored as a string in the DB. E.g.,
    2.813T for 2813000000000. This method simply formats this entry as a
    numeric value. If T appears then the T will be trimmed, the entry
    will be converted to numeric and multiplied by 1 trillion.
    
    Parameters:
    df (DataFrame) : Pass the series rather than the full DataFrame.
            This series will be 
            
    Returns:
    df (DataFrame) : The updated DataFrame with MARKET_CAP formatted as a
            numeric columns.
    '''
