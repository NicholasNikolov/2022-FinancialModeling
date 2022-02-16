

from nltk.sentiment.vader import SentimentIntensityAnalyzer

new_words = {
    'grew': 1.0,
    'grow': 1.0,
}

SIA = SentimentIntensityAnalyzer()

SIA.lexicon.update(new_words)