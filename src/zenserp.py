# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 20:35:07 2022

@author: nikol
"""
import zenserp

class zenserp_client(object):
    def __init__(self):
        self.client = self.establish_zenserp_client()
        
    def establish_zenserp_client(self):
        print("src.zenserp.establish_zenserp_client()")
        '''
        Establish the API client with the appropriate API key.
        '''
        API_KEY = '2d3e1b70-8887-11ec-9541-fdb5a8979f9d'
        client = zenserp.Client(API_KEY)
        
        return client
    
    def search_google(self , ticker):
        print("Running src.zenserp.search_google")
        '''
        Perform the zenserp search
        '''
        client = self.client
        
        params = (
            ('q', ticker),
            ('location', 'United States'),
            ('search_engine', 'google.com'),
            ('num' , '20'),
            ('tbm' , 'nws'),
        )
        
        
        result = client.search(params)
        return result
    
    def extract_description(self , result):
        print("Running src.zenserp.extract_descrition")
        '''
        '''
        
        description_list = [result['news_results'][index]['description'] 
                            for index in range(len(result['news_results']))]
        
        return description_list
    
    def batch_search(self , ticker_symbols):
        print("Running src.zenserp.batch_search")
        '''
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