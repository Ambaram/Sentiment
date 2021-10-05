from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from requests.sessions import session
import tweepy
from textblob import TextBlob
import pandas as pd
import re


class Tweets:
    def __init__(self, q):
        self.q = q

    def get_tweet(self):
        authenticate = tweepy.OAuthHandler(
            "5UaECoouWDZnPhka0ad4fI48r", "Nv3Gp5A8ME2GpzRZeN0va9BVo7rNLDsjv4eur04Hi6kegSOr3G")
        authenticate.set_access_token(
            "2685636744-wUKIayVLjweyi7YVGvL3SBWe8bUgAf3QT2TZfAD", "awEEfMZjb6AaOHK0LXeDAJgPIWTCyyVnFp2ydSkDa4Bwi")
        api = tweepy.API(authenticate, wait_on_rate_limit=True)
        data = api.search_tweets(
            q=self.q, count=5, lang='en', tweet_mode='extended')
        df = pd.DataFrame(
            [tweets.full_text for tweets in data], columns=['Tweets'])

        def clean_text(text):
            text = re.sub(r'RT[\s]+', '', text)
            text = re.sub(r'@[A-Za-z0-9\_\:]+', '', text)
            text = re.sub(r'\:\-\)\+', '', text)
            return text
        df['Tweets'] = df['Tweets'].apply(clean_text)

        def getSubjectivity(text):
            return TextBlob(text).sentiment.subjectivity

        def getPolarity(text):
            return TextBlob(text).sentiment.polarity
        df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
        df['Polarity'] = df['Tweets'].apply(getPolarity)

        def getSentiment(text):
            if text > 0:
                return "Positive"
            elif text == 0:
                return "Neutral"
            else:
                return "Negative"
        df['Sentiment'] = df['Polarity'].apply(getSentiment)
        return df[['Tweets', 'Sentiment']]
