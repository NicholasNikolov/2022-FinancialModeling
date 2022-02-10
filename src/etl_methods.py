# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 20:33:38 2022
@author: Nicholas Nikolov

These methods focus on the webscraping and data prep for loading into the 
database. This includes initial entry methods like get_parameters.
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import time

import src.db_connection as db
import src.zenserp as zs


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
        
        time.sleep(5)

    return data_dict

def update_ticker_symbols_db(ticker_symbols):
    print("Running src.etl_methods.update_ticker_symbols_db")
    '''
    When ticker_symbols list is passed, this method will attempt to input the symbols
    into the ticker_symbols table in the DB. This logs all ticker symbols that have
    ever been input in the financial_data table. If the ticker already exists
    in the table then it will not be input. If it does not exist then the new
    ticker will be input.
    
    Method uses the batch query to write multiple queries before committing the DB.
    
    Parameters:
    ticker_symbols (list) : The list of ticker symbols that is being used for the
            web scrape and data creation.
            
    Returns:
    None
    '''
    db_connect = db.db_methods()
    query = "INSERT IGNORE INTO yh_finance_db.ticker_symbols (symbol_name) VALUES (%s)"
    param_list = ticker_symbols
    db_connect.batch_write_query(query , param_list)
    
    
def generate_zenserp_dict(ticker_symbols):
    print("Running src.etl_methods.generate_zenserp_dict")
    '''
    Create the zenserp_dict. This dictionary is formatted as follows:
        
        {"SYMBOL" : ['sentence1' , 'sentence2']}
    
    In the above, SYMBOL represents the ticker symbol (e.g., AAPL) and each
    sentence is a web-scraped description from the Google search engine. The whole
    process is done via Zenserp which cleanly organizes the top searches. 
    
    Parameters:
    ticker_symbols (list) : The list of ticker symbols to use for the query.
    
    Returns:
    zenserp_dict (dict) : The Zenserp dictionary formatted as described in the
            summary above.
    '''
    # Declare the Zenserp object
    zenserp_client = zs.zenserp_client()
    
    # Use the Zenserp batch query to extract all ticker symbols being studied.
    zenserp_dict = zenserp_client.batch_search(ticker_symbols)
    
    return zenserp_dict

def merge_data(data_dict , sentiment_dict):
    print("Running src.etl_methods.merge_data")
    '''
    Merge the data_dict and the Zenserp sentiment_dict into a single unified dictionary.
    The data_dict contains all data extracted from the webscrape of Yahoo! Finance.
    The sentiment_dict contains the data extracted from the Google Search news
    results. Both dictionaries should be merged in order to generate the SQL
    query and only run one query to the DB.
    
    Parameters:
    data_dict (dict) : The dictionary containing the data extracted from
            Yahoo! Finance.
            
    sentiment_dict (dict) : The dictionary containing the data extracted
            from the Zenserp Google search.
            
    returns:
        data_dict (dict) : data_dict itself is updated with the sentiment_dict
                data and returned.
    '''
    
    for ticker in data_dict.keys():
        data_dict[ticker].update(sentiment_dict[ticker])
        
    return data_dict
    

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
    
    db_connect = db.db_methods()
    query = "select * from yh_finance_db.ticker_symbols"
    params = []
    ticker_result = db_connect.db_read(query , params)
    ticker_result = {tick['symbol_name'] : tick['ID'] for tick in ticker_result}
    
    query = '''insert into yh_finance_db.financial_data (ticker_symbol_id , TICKER_SYMBOL , DATE_TIME , PREV_CLOSE,
    OPEN, BID, ASK, DAYS_RANGE, FIFTY_TWO_WK_RANGE, TD_VOLUME, AVERAGE_VOLUME_3MONTH,
    MARKET_CAP, BETA_5Y, PE_RATIO, EPS_RATIO, EARNINGS_DATE, DIVIDEND_AND_YIELD,
    EX_DIVIDEND_DATE, ONE_YEAR_TARGET_PRICE , SENTIMENT_NEG , SENTIMENT_NEU , 
    SENTIMENT_POS , SENTIMENT_COMPOUND) VALUES (%s , %s , NOW() , %s , %s , %s ,
                                                     %s , %s , %s , %s , %s ,
                                                     %s , %s , %s , %s , %s ,
                                                     %s , %s , %s , %s , %s ,
                                                     %s , %s)'''
    
    param_list = []
    for ticker in data_dict.keys():
        ticker_symbol_id = ticker_result[ticker]
        param_list.append([ticker_symbol_id , ticker , data_dict[ticker]['PREV_CLOSE'],
                       data_dict[ticker]['OPEN'] , data_dict[ticker]['BID'] , 
                       data_dict[ticker]['ASK'] , data_dict[ticker]['DAYS_RANGE'] , 
                       data_dict[ticker]['FIFTY_TWO_WK_RANGE'] , 
                       data_dict[ticker]['TD_VOLUME'] , data_dict[ticker]['AVERAGE_VOLUME_3MONTH'] , 
                       data_dict[ticker]['MARKET_CAP'] , data_dict[ticker]['BETA_5Y'] ,
                       data_dict[ticker]['PE_RATIO'] , data_dict[ticker]['EPS_RATIO'] ,
                       data_dict[ticker]['EARNINGS_DATE'] , data_dict[ticker]['DIVIDEND_AND_YIELD'] , 
                       data_dict[ticker]['EX_DIVIDEND_DATE'] , data_dict[ticker]['ONE_YEAR_TARGET_PRICE'] ,
                       data_dict[ticker]['SENTIMENT_NEG'] , data_dict[ticker]['SENTIMENT_NEU'] , 
                       data_dict[ticker]['SENTIMENT_POS'] , data_dict[ticker]['SENTIMENT_COMPOUND']
                       ])
                                      
    db_connect.batch_write_query(query , param_list)            


        