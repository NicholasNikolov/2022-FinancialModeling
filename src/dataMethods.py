# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 20:33:38 2022

@author: nikol
"""

import requests
from bs4 import BeautifulSoup
import json
import os




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
        return_dict[dt] = found_value

    return return_dict

        