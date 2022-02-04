# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 21:22:02 2022

@author: nikol
"""
import os

os.chdir("C:\\Users\\nikol\\OneDrive\\Professional\\Learning\\2022-Financial_Scrape_and_Forecast")
import src.dataMethods as dm

parameters = dm.get_parameters()

def run_data_populater(parameters):
    print("Running run_data_populater")
    
    '''
    Main method for populating extracted data into the DB.
    '''
    
    # Declare the variables.
    data_list = parameters['data_list']
    ticker_symbols = parameters["ticker_symbols"]
    return_dict = {}
    
   
    for ticker in ticker_symbols:
        # Generate the link using the provided ticker symbol.
        link = dm.generate_link(ticker)
        entry_dict = dm.get_html(link , data_list)
        
        # Populate the return dictionary that contains values for all tickers.
        return_dict[ticker] = entry_dict
    
    return return_dict
    
test = run_data_populater(parameters)