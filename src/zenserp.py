# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 20:35:07 2022

@author: nikol
"""
import zenserp
import os

class zenserp_client(object):
    def __init__(self):
        self.client = self.establish_zenserp_client()
        
    def establish_zenserp_client(self):
        print("src.zenserp.establish_zenserp_client")
        '''
        Establish the API client with the appropriate API key.
        
        Parameters:
        None
        
        Returns:
        client (zenserp.Client) : The active Zenserp client connected to the
                relevant API.
        '''
        
        # Pull the API key from the environmental variables.
        API_KEY = os.getenv('ZENSERP_API')
        
        # Establish the Zenserp client.
        client = zenserp.Client(API_KEY)
        
        return client
    
    def search_google(self , ticker):
        print("Running src.zenserp.search_google")
        '''
        Perform the zenserp search and return the result of a single query.
        
        Parameters:
        ticker (str) : The ticker being searched for in Google.
        
        Returns:
        result (dict) : The dictionary containing the full search results gathered
                by Zenserp.
        '''
        client = self.client
        
        params = (
            ('q', ticker),
            ('location', 'United States'),
            ('search_engine', 'google.com'),
            ('num' , '5'),
            ('tbm' , 'nws'),
        )
        
        
        result = client.search(params)
        
        return result
    
    def extract_description(self , result):
        print("Running src.zenserp.extract_descrition")
        '''
        Extract the descriptions from the resulting search and format as a list.
        
        Parameters:
        result (dict) : The result from the single Zenserp query to Google.
        
        Returns:
        description_list (list) : The list of descriptions. These descriptions are
                the short descriptions found when performing a Google search.
        '''
        
        description_list = [result['news_results'][index]['description'] 
                            for index in range(len(result['news_results']))]
        
        return description_list
    
    def batch_search(self , ticker_symbols):
        print("Running src.zenserp.batch_search")
        '''
        Perform a batch search for a list of ticker symbols. This method will
        call on the search_google method within this class in order to get
        results for the full list of ticker symbols. The results will then be
        formatted into zenserp_return_dict with the ticker symbols as keys.
        
        Parameters:
        ticker_symbols (list) : The list of ticker symbols being used to query.
        
        Returns:
        zenserp_return_dict (dict) : The dictionary containing the full
                data from the search with the ticker symbols as keys.
        '''
        
        zenserp_return_dict = {}
        
        for ticker in ticker_symbols:
            result = self.search_google(ticker)
            description_list = self.extract_description(result)
            zenserp_return_dict[ticker] = description_list
            
        return zenserp_return_dict
    

if __name__ == '__main__':
    ### TESTING ###
    client = zenserp_client()
    result = client.search_google("AAPL")
    ### TESTING ###