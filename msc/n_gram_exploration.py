# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 20:14:21 2022

@author: nikol
"""

from textblob import TextBlob

def find_ngrams(n, input_sequence):
    # Split sentence into tokens.
    tokens = input_sequence.split()
    ngrams = []
    for i in range(len(tokens) - n + 1):
        # Take n consecutive tokens in array.
        ngram = tokens[i:i+n]
        # Concatenate array items into string.
        ngram = ' '.join(ngram)
        ngrams.append(ngram)

    return ngrams

my_string = "This product is very good, you should try it"

ngrams = find_ngrams(3, my_string)
analysis = {}
for ngram in ngrams:
    blob = TextBlob(ngram)
    print('Ngram: {}'.format(ngram))
    print('Polarity: {}'.format(blob.sentiment.polarity))
    print('Subjectivity: {}'.format(blob.sentiment.subjectivity))