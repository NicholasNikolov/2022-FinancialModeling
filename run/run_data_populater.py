# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 21:22:02 2022

@author: Nicholas Nikolov
"""
import os

os.chdir("C:\\Users\\nikol\\OneDrive\\Professional\\Learning\\2022-Financial_Scrape_and_Forecast")

import src.etl_methods as etl
import src.sentiment_analysis as sa

parameters = etl.get_parameters()

def run_data_populater(parameters):
    print("Running run_data_populater")
    
    '''
    Main method for populating extracted data into the DB.
    '''
    
    # Declare the variables
    data_list = parameters['data_list']
    ticker_symbols = parameters["ticker_symbols"]
    
    # Update the DB dict
    etl.update_ticker_symbols_db(ticker_symbols)
    
    # The data dictionary containing the base Yahoo! Finance data
    return_dict = etl.generate_data_dict(data_list , ticker_symbols)
    
    # Zenserp 
    zenserp_dict = etl.generate_zenserp_dict(ticker_symbols)
    
    # Sentiment Analysis
    sentiment_dict = sa.determine_sentiments_from_dict(zenserp_dict)
    
    # Computes the sentiment averages by sentiment level
    sentiment_averages = sa.compute_sentiment_averages(sentiment_dict)
    
    # Merges sentiment_averages to the return_dict
    merged_data = etl.merge_data(return_dict , sentiment_averages)
    
    # Uploads all scraped data to the DB
    upload_query = etl.upload_extracted_data(merged_data)
    
    return return_dict


test = run_data_populater(parameters)

# {'neu':'1'}