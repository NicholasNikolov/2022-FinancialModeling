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
    
    data_list = parameters['data_list']
    ticker_symbols = parameters["ticker_symbols"]
    
    link = dm.generate_link("AAPL")
    entry_dict = dm.get_html(link , data_list)
    
    return entry_dict
    
test = run_data_populater(parameters)