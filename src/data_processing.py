# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 14:05:53 2022
@author: Nicholas Nikolov

These methods perform the data processing to prepare the data for modeling.
This includes interpolating nulls, determining datatypes, formatting strings, etc.
"""

import src.db_connection as db
import pandas as pd

# =============================================================================
# WARNING SUPPRESSION
# =============================================================================
pd.options.mode.chained_assignment = None
# =============================================================================
# WARNING SUPPRESSION
# =============================================================================

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
    
    # Remove the commas to allow for conversion to int.
    df.TD_VOLUME = df.TD_VOLUME.str.replace(',' , '')
    
    # Convert the column to int.
    df.TD_VOLUME = df.TD_VOLUME.astype(int)
    
    return df

def process_AVERAGE_VOLUME_3MONTH(df):
    print("Running src.data_processing.process_TD_VOLUME")
    '''
    Process AVERAGE_VOLUMNE_3MONTH. Entries in this feature column contain commas.
    The method replaces these commas to allow for conversion to int. Then the
    column is converted to int.
    
    Parameters:
    df (DataFrame) : The DataFrame to be processed.
    
    Returns:
    df (DataFrame) : The processed DataFrame.
    '''
    
    # Remove the commas to allow for conversion to int.
    df.AVERAGE_VOLUME_3MONTH = df.AVERAGE_VOLUME_3MONTH.str.replace(',' , '')
    
    # Convert the column to int.
    df.AVERAGE_VOLUME_3MONTH = df.AVERAGE_VOLUME_3MONTH.astype(int)
    
    return df


def process_MARKET_CAP(df):
    print("src.data_processing.process_MARKET_CAP")
    '''
    Process the MARKET_CAP feature. This data is presented as a string with M,
    B, or T appended at the end for million, billion, or trillion.
    Because there is a possibility for there to be a mix of entries, I loop 
    through the column and make updates on an entry-by-entry basis, rather than
    updating the full column at once.
    
    Each entry has the appended letter removed, is converted to a float, and is
    multiplied by the correct multiple. E.g., 1000000 for million (or M).
    
    Parameters:
    df (DataFrame) : The dataframe that will be processed.
    
    Returns:
    df (DataFrame) : The df with MARKET_CAP processed and dtype converted to float.
    '''
    
    # Convert the text format into float-compatible format.
    for index in range(len(df.MARKET_CAP)):
        if "T" in df.MARKET_CAP[index]:
            entry_float = float(df.MARKET_CAP[index].replace("T",""))
            df.MARKET_CAP[index] = entry_float * 1000000000000
            
        elif "B" in df.MARKET_CAP[index]:
            entry_float = float(df.MARKET_CAP[index].replace("B",""))
            df.MARKET_CAP[index] = entry_float * 1000000000
            
        elif "M" in df.MARKET_CAP[index]:
            entry_float = float(df.MARKET_CAP[index].replace("M",""))
            df.MARKET_CAP[index] = entry_float * 1000000
            
    # Convert the whole column into float64.
    df.MARKET_CAP = df.MARKET_CAP.astype(float)
    
    return df


def process_float_stats(df):
    print("Running src.data_processing.process_float_stats")
    '''
    Process all statistics that are already formatted as floats but need the
    column type updated.
    
    Parameters:
    df (DataFrame) : The DataFrame containing the relevant features.
    
    Returns:
    df (DataFrame) : The DataFrame with the relevant features converted to floats.
    
    Future Work:
    Determine these dtypes in advance. Naturally some columns must read in as
    objects (unless the data processing occurs in SQL within the DB which is
             more proper but will require more time)
    '''
    
    df.BETA_5Y = df.BETA_5Y.astype(float)
    df.PE_RATIO = df.PE_RATIO.astype(float)
    df.EPS_RATIO = df.EPS_RATIO.astype(float)
    df.ONE_YEAR_TARGET_PRICE = df.ONE_YEAR_TARGET_PRICE.astype(float)
    df.SENTIMENT_NEG = df.SENTIMENT_NEG.astype(float)
    df.SENTIMENT_NEU = df.SENTIMENT_NEU.astype(float)
    df.SENTIMENT_POS = df.SENTIMENT_POS.astype(float)
    df.SENTIMENT_COMPOUND = df.SENTIMENT_COMPOUND.astype(float)
    
    return df

def format_timestamp(df, time_stamp_column):
    print("Running src.data_processing.format_timestamp")
    '''
    '''
    # Format the datetime.
    df[time_stamp_column] = pd.to_datetime(df[time_stamp_column])

    return df



if __name__ == '__main__':
    
    df = read_format_df('AAPL')
    
    df = prepare_data(df)




























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
