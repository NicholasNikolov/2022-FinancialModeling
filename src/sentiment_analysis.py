# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 21:46:45 2022

@author: nikol
"""

from nltk.sentiment import SentimentIntensityAnalyzer


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
    
    if return_all == False:
        compound = polarity_dict['compound']
        return compound
    else:
        #return neg , neu , pos , compound
        return polarity_dict
    
def determine_overall_sentiment(description_list):
    print("Running src.sentiment_analysis.format_sentiment_dict")
    '''
    Calculate the sentiment scores from sentences in the description list.
    
    Parameters:
    description_list (list) : List of sentences pulled from the zenserp client.
    
    Returns:
    sentiment_scores (list) : List of sentiment scores for the sentences that
            were in description_list.
    '''
    
    sentiment_scores = [determine_sentiment(description , return_all = True) for description in description_list]
    
    return sentiment_scores

def compute_sentiment_averages(sentiment_dict):
    print("Running src.sentiment_analysis.compute_sentiment_averages()")
    '''
    Compute an average for all independent sentiments collected for each sentence.
    Recall that the zenserp client is pulling multiple sentiments at once. This
    method will take the average score of those methods for the negative, neutral, 
    positive, and compound.
    
    Parameters:
    sentiment_dict (dict) : Dictionary containing the sentiment scores for each
            ticker symbol. Within those it contains the sentences.
            
    Returns:
    sentiment_averages (dict) : The average sentiment scores for each ticker.
            Includes the neg, neu, pos, and comp averages.
    '''
    
    sentiment_averages = {}
    for ticker in sentiment_dict.keys():
        full_list = sentiment_dict[ticker]
        
        neg_avg = sum(val['neg'] for val in full_list) / len(full_list)
        neu_avg = sum(val['neu'] for val in full_list) / len(full_list)
        pos_avg = sum(val['pos'] for val in full_list) / len(full_list)
        comp_avg = sum(val['compound'] for val in full_list) / len(full_list)
        
        sentiment_averages[ticker] = {'SENTIMENT_NEG' : neg_avg}
        sentiment_averages[ticker]['SENTIMENT_NEU'] = neu_avg
        sentiment_averages[ticker]['SENTIMENT_POS'] = pos_avg
        sentiment_averages[ticker]['SENTIMENT_COMPOUND'] = comp_avg
        
    return sentiment_averages
    
    
def determine_sentiments_from_dict(zenserp_dict):
    print("src.sentiment_analysis.determine_sentiments_from_dict")
    '''
    Build out the sentiment dictionary using the sentence dictionary produced
    by the senzerp client.
    
    Parameters:
    zenserp_dict (dict) : The dictionary produced from running the zenserp client.
            Contains the ticker symbols as keys and the sentences scraped as
            the values.
            
    Returns:
    sentiment_dict (dict) : The dictionary containing all sentiments for the
            tickers and each contained sentence. These are raw scores and not
            averages.
    '''
    
    sentiment_dict = {}
    
    for ticker in zenserp_dict.keys():
        sentiment_scores = determine_overall_sentiment(zenserp_dict[ticker])
        sentiment_dict[ticker] = sentiment_scores
    
    return sentiment_dict