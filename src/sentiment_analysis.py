# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 21:46:45 2022

@author: nikol
"""

from nltk.sentiment import SentimentIntensityAnalyzer
import src.zenserp as zs

def determine_sentiment(sentence , return_all = False):
    print("Running src.sentiment_analysis.determine_sentiment")
    '''
    Determine sentiment scoring based on Valence Aware Dictionary and
    Sentiment Reasoner (VADER). By default only compound score is returned
    but will likely return all sentiment scoring for more data.
    
    Parameters:
    sentence (str) : Single string sentence containing the text to be
            analyzed.
            
    return_all (bool) : Whether or not to return all results or just the
            compound score.
    '''
    
    sia = SentimentIntensityAnalyzer()
    
    polarity_dict = sia.polarity_scores(sentence)
    
    neg = polarity_dict['neg']
    neu = polarity_dict['neu']
    pos = polarity_dict['pos']
    compound = polarity_dict['compound']
    
    if return_all == False:
        return compound
    else:
        return neg , neu , pos , compound
    
def determine_overall_sentiment(description_list):
    print("Running src.sentiment_analysis.format_sentiment_dict")
    '''
    '''
    
    description_list = zs.extract_description()
    
    sentiment_scores = [determine_sentiment(description)
        for description in description_list]