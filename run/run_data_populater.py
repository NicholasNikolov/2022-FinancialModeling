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
    
    # Update the DB dict
    dm.update_ticker_symbols_db(ticker_symbols)

    return_dict = dm.generate_data_dict(data_list , ticker_symbols)
    
    upload_query = dm.upload_extracted_data(return_dict)
    
    return return_dict


test = run_data_populater(parameters)