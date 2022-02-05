# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 20:33:38 2022

@author: nikol
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import time

import src.db_connection as db




def get_parameters(file_path = 'dct/parameters.json'):
    print("Running get_parameters")
    '''
    Extracts the parameters used throughout the data population code.
    
    Parameters:
    file_path (str) : the filepath. Defaults to the dct folder.
    
    Returns:
    parameters (dict) : Dictionary return of the parameters extracted from the
            .json file designated in the filepath.
    '''
    
    with open("dct/parameters.json", 'r') as j:
        parameters = json.loads(j.read())
        
    return parameters

def generate_link(ticker_symbol):
    print("Running generate_link")
    '''
    Generate a link based on the provided ticker symbol. This link will be used
    to access the Yahoo! Finance website and extract relevant data. Assumption
    is that the website will follow a standard format.
    
    Parameters:
    ticker_symbol (str) : The ticker symbol that is being used for data pop.
    
    Returns:
    '''
    
    link = "https://finance.yahoo.com/quote/{}?p={}&.tsrc=fin-srch".format(ticker_symbol , 
                                                                    ticker_symbol)
    
    return link

def get_html(link , data_list):
    print("Running get_html")
    '''
    Get the HTML and perform initial processing on it.
    
    Parameters:
    link (str) : The link for which to extract the text values. In the context
            of Yahoo! Finance, this will be the URL to the page containing the
            relevant data for each stock being studied.
            
    data_list (list) : The list containing the specific labels containing the 
            data to be extracted.
        
    Returns:
    return_dict (dict) : The dictionary with the values from data_list as keys
            and the relevant extracted data as the value. E.g., "OPEN-value" : 174
    '''
    
    return_dict = {}
    NewResponse = requests.get(link)
    html = BeautifulSoup(NewResponse.text,'html.parser')
    
    for dt in data_list:
        found_value = html.find('td' , {'data-test' : dt}).text.strip()
        
        # Clean -value from dt
        dt = dt.replace("-value", "")

        
        return_dict[dt] = found_value

    return return_dict

def generate_data_dict(data_list , ticker_symbols):
    print("Running src.dataMethods.generate_data_dict")
    '''
    Loops through the ticker_symbols and performs webscrape on Yahoo! Finance
    to pull data in. The format is as follows:
        
        {"Ticker_symbol" : {"data_1" : "value" , "data2" : "value"} ,
         "Ticker_symbol2" : {"data_1" : "value" , "data2" : "value"}}
        
    Parameters:
    data_list (list) : List of entries to be populated. E.g., Earnings Date,
            Open and Close, Dividend yield...
            
    ticker_symbols (list) : The list of ticker symbols being used.
    
    Returns:
    data_dict (dict) : The dictionary containing the relevant data formatted
            as described in the summary above.
    '''
    data_dict = {}
    for ticker in ticker_symbols:
        # Generate the link using the provided ticker symbol.
        link = generate_link(ticker)
        entry_dict = get_html(link , data_list)
        
        # Populate the return dictionary that contains values for all tickers.
        data_dict[ticker] = entry_dict

    return data_dict

def update_ticker_symbols_db(ticker_symbols):
    
    query = "INSERT IGNORE INTO yh_finance_db.ticker_symbols (symbol_name) VALUES (%s)"
    param_list = ticker_symbols
    db.batch_write_query(query , param_list)
    
    
    
    # for ticker in ticker_symbols:
    #     query = "INSERT IGNORE INTO yh_finance_db.ticker_symbols (symbol_name) VALUES (%s)"
    #     params = [ticker]
    #     db.db_write(query , params)
    

def upload_extracted_data(data_dict):
    print("Running src.dataMethods.build_data_upload_query")
    '''
    Converts the data dictionary into a SQL query that can be applied to the
    database.
    
    Parameters:
    data_dict (dict) : The output dictionary from generate_data_dict. Formatted
            as shown in the summary of generate_data_dict.
            
    Returns:
    data_input_query (str) : The SQL query for data upload to the database.
    '''
    
    query = "select * from yh_finance_db.ticker_symbols"
    params = []
    ticker_result = db.db_read(query , params)
    ticker_result = {tick['symbol_name'] : tick['ID'] for tick in ticker_result}
    
    query = '''insert into yh_finance_db.financial_data (ticker_symbol_id , DATE_TIME , PREV_CLOSE,
    OPEN, BID, ASK, DAYS_RANGE, FIFTY_TWO_WK_RANGE, TD_VOLUME, AVERAGE_VOLUME_3MONTH,
    MARKET_CAP, BETA_5Y, PE_RATIO, EPS_RATIO, EARNINGS_DATE, DIVIDEND_AND_YIELD,
    EX_DIVIDEND_DATE, ONE_YEAR_TARGET_PRICE) VALUES (%s , NOW() , %s , %s , %s ,
                                                     %s , %s , %s , %s , %s ,
                                                     %s , %s , %s , %s , %s ,
                                                     %s , %s , %s)'''
    
    param_list = []
    for ticker in data_dict.keys():
        ticker_symbol_id = ticker
        param_list.append([ticker_symbol_id , data_dict[ticker]['PREV_CLOSE'],
                       data_dict[ticker]['OPEN'] , data_dict[ticker]['BID'] , 
                       data_dict[ticker]['ASK'] , data_dict[ticker]['DAYS_RANGE'] , 
                       data_dict[ticker]['FIFTY_TWO_WK_RANGE'] , 
                       data_dict[ticker]['TD_VOLUME'] , data_dict[ticker]['AVERAGE_VOLUME_3MONTH'] , 
                       data_dict[ticker]['MARKET_CAP'] , data_dict[ticker]['BETA_5Y'] ,
                       data_dict[ticker]['PE_RATIO'] , data_dict[ticker]['EPS_RATIO'] ,
                       data_dict[ticker]['EARNINGS_DATE'] , data_dict[ticker]['DIVIDEND_AND_YIELD'] , 
                       data_dict[ticker]['EX_DIVIDEND_DATE'] , data_dict[ticker]['ONE_YEAR_TARGET_PRICE']
                       ])
                                      
    db.batch_write_query(query , param_list)            
    

    

        