# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 20:35:07 2022

@author: nikol
"""
import zenserp

def establish_zenserp_client():
    print("src.zenserp.establish_zenserp_client()")
    '''
    '''
    API_KEY = '2d3e1b70-8887-11ec-9541-fdb5a8979f9d'
    client = zenserp.client(API_KEY)