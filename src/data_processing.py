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


def prepare_data(df):
    print("Running src.data_processing.establish_data_types")
    '''
    Pre-process data to prepare it for modeling in later stage.
    Many of the included methods may eventually be performed within
    the SQL DB. This is a manual process. I can come up with automatic
    data processing steps but I don't see a use at this time.
    
    Parameters:
    df (DataFrame) : The pandas DataFrame that will be pre-processed.
    
    '''
    
    df = process_PREV_CLOSE(df)
    
    df = process_OPEN(df)
    
    df = process_DAYS_RANGE(df)
    
    df = process_FIFTY_TWO_WK_RANGE(df)
    
    df = process_TD_VOLUME(df)
    
    df = process_AVERAGE_VOLUME_3MONTH(df)


def process_PREV_CLOSE(df):
    print("Running src.data_processing.process_PREV_CLOSE")
    '''
    '''
    
    df.PREV_CLOSE = pd.to_numeric(df.PREV_CLOSE, errors='coerce')
    
    return df


def process_OPEN(df):
    print("Running src.data_processing.process_OPEN")
    '''
    '''
    
    df.OPEN = pd.to_numeric(df.OPEN, errors='coerce')
    
    return df


def process_DAYS_RANGE(df):
    print("Running src.data_processing.process_DAYS_RANGE")
    '''
    '''
    
    split_DAYS_RANGE = df.DAYS_RANGE.str.split(pat = ' - ' , expand = True)
    split_DAYS_RANGE.columns = ['DAYS_RANGE_lower' , 'DAYS_RANGE_higher']
    
    dfc = pd.concat([df , split_DAYS_RANGE] , axis = 1)
    
    dfc.DAYS_RANGE_lower = pd.to_numeric(dfc.DAYS_RANGE_lower , errors = 'coerce')
    dfc.DAYS_RANGE_higher = pd.to_numeric(dfc.DAYS_RANGE_higher , errors = 'coerce')
    
    return dfc


def process_FIFTY_TWO_WK_RANGE(df):
    print("Running src.data_processing.process_DAYS_RANGE")
    '''
    '''
    
    split_FIFTY_TWO_WK_RANGE = df.FIFTY_TWO_WK_RANGE.str.split(pat = ' - ' , expand = True)
    split_FIFTY_TWO_WK_RANGE.columns = ['FIFTY_TWO_WK_RANGE_lower' , 'FIFTY_TWO_WK_RANGE_higher']
    
    dfc = pd.concat([df , split_FIFTY_TWO_WK_RANGE] , axis = 1)
    
    dfc.FIFTY_TWO_WK_RANGE_lower = pd.to_numeric(dfc.FIFTY_TWO_WK_RANGE_lower , errors = 'coerce')
    dfc.FIFTY_TWO_WK_RANGE_higher = pd.to_numeric(dfc.FIFTY_TWO_WK_RANGE_higher , errors = 'coerce')
    
    return dfc


def process_TD_VOLUME(df):
    print("Running src.data_processing.process_TD_VOLUME")
    '''
    '''
    
    df.TD_VOLUME = df.TD_VOLUME.str.replace(',' , '')
    
    return df

def process_AVERAGE_VOLUME_3MONTH(df):
    print("Running src.data_processing.process_TD_VOLUME")
    '''
    '''
    
    df.AVERAGE_VOLUME_3MONTH = df.AVERAGE_VOLUME_3MONTH.str.replace(',' , '')
    
    return df





def format_timestamp(df, time_stamp_column):
    print("Running src.data_processing.format_timestamp")
    '''
    '''
    # Format the datetime.
    df[time_stamp_column] = pd.to_datetime(df[time_stamp_column])

    return df

































# =============================================================================
# def interpolate_nulls(df):
#     print("Running src.data_processing.interpolate_nulls()")
#     '''
#     Fill missing null values based on the most recent values surrounding the
#     null entry. Data interpolation works by taking an average of the value
#     immediately preceding the null and the one immediately after. In cases
#     of multiple nulls in a row, the interpolater should set all nulls to the
#     same average.
#     '''
# 
# 
# def MARKET_CAP_to_numeric(df):
#     print("Running src.data_processing.MARKET_CAP_to_numeric")
#     '''
#     Format MARKET_CAP properly. It is stored as a string in the DB. E.g.,
#     2.813T for 2813000000000. This method simply formats this entry as a
#     numeric value. If T appears then the T will be trimmed, the entry
#     will be converted to numeric and multiplied by 1 trillion.
#     
#     Parameters:
#     df (DataFrame) : Pass the series rather than the full DataFrame.
#             This series will be 
#             
#     Returns:
#     df (DataFrame) : The updated DataFrame with MARKET_CAP formatted as a
#             numeric columns.
#     '''
# =============================================================================
