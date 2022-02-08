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
            ('num' , '5'),
            ('tbm' , 'nws'),
        )
        
        
        result = client.search(params)
        return result