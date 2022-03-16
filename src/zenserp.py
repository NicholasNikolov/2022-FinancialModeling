# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 20:35:07 2022

@author: nikol
"""
import zenserp
import os
from GoogleNews import GoogleNews
import time

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
        
        time.sleep(25)
        result = client.search(params)
        
        # March change to Google search caused some search queries to fail. This
        # try except clause will reattempt the search five times before giving up.
        # Hopefully this allows me to gather the necessary data more reliably.
        try:
            result['news_results']
        except KeyError:
            reattempt_count = 1
            
            while reattempt_count <= 5 and 'news_results' not in result.keys():
                print("Zenserp Search Failed. Trying again. Attempt " + str(reattempt_count))
                
                time.sleep(10)
                result = client.search(params)
                reattempt_count += 1
        
        return result
    
    def extract_description(self , result , ticker):
        print("Running src.zenserp.extract_description")
        '''
        Extract the descriptions from the resulting search and format as a list.
        
        Parameters:
        result (dict) : The result from the single Zenserp query to Google.
        
        Returns:
        description_list (list) : The list of descriptions. These descriptions are
                the short descriptions found when performing a Google search.
        '''
        
        try:
            description_list = [result['news_results'][index]['description'] 
                                for index in range(len(result['news_results']))]
            
        except:
            print("Zenserp client failed. Trying with GoogleNews module.")
            description_list = self.handle_zenserp_exception(ticker)
        
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
            description_list = self.extract_description(result , ticker)
            zenserp_return_dict[ticker] = description_list
            
        return zenserp_return_dict
    
    def handle_zenserp_exception(self , ticker):
        print("Running src.zenserp.handle_zenserp_exception")
        '''
        Zenserp failure of news search is causing issues in data collection.
        There have been instances of search failure that are the fault of the
        Zenserp API. I have created a method to handle these exceptions and extract
        the proper text.
        
        Parameters:
        ticker (str) : The search ticker to be looked up.
        
        Returns:
        description_list (list) : The list of sentence summaries on the news page.
        '''
        time.sleep(25)
        nws = GoogleNews()
        nws.search(ticker)
        
        description_list = nws.get_texts()[:5]
        
        # !!! Temporary solution. For some reason the search result is returning
        # as empty.
        # !!! Need to create proper checks for empty lists to search for the result
        # again. Unclear why it's failing for zenserp AND GoogleNews().
        # I think there was a change in the google search engine because both
        # zenserp and GoogleNews() are having issue. Seems that some queries
        # fail to extract the actual top news articles. It's unclear what
        # causes this to happen. Might explore exceptions that try a different
        # search engine.
        # The solution is very strange. The search might fail the first and 
        # second time but then may succeed the third time.. 
        try:
            5/len(description_list)
        except:
            nws.search(ticker)
            
            description_list = nws.get_texts()[:5]

            nws.search(ticker)
            
            description_list = nws.get_texts()[:5]

            nws.search(ticker)
            
            description_list = nws.get_texts()[:5]


        
        return description_list
        
    

if __name__ == '__main__':
    ### TESTING ###
    client = zenserp_client()
    result = client.search_google("AAPL")
    ### TESTING ###