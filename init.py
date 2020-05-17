import pandas as pd
import tweepy
import os
from Data_Gathering.twitter_data import get_corona_tweets
from Processing.sentiment_analysis import Classifier


class InitApplication:
    def __init__(self):
        self.api = self.init_tweepy_api()
        self.classifier = Classifier()

    def init_tweepy_api(self):
        # Consumer keys and access tokens, used for OAuth
        from Frontend.api import app
        consumer_key = "cOjc6hE5gxMcNedk3y9u3OR0o"
        consumer_secret = "CM54GTZTEpGwxcwedZicIjckLtyYk10pQ8K54FEvM5tHf3zmMA"
        access_token = "1246038981038477317-wzYjLQUgx9qJHJQPtDqMjKSjbSCO3a"
        access_token_secret = "SncxBqMu3OVBetdkROr8cpD2wq7DojGMNC2EYyUR3o1Mo"

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        # Calling the api
        return tweepy.API(auth)

    def create_tweet_data(self):
        all_tweets = get_corona_tweets(base_dir=os.getcwd())
        clf = Classifier()
        all_tweets['sentiment'] = pd.Series(clf.get_sentiment(all_tweets['cleaned_text']), index=all_tweets.index)
        return all_tweets



# Starting the Flask app
#app.run()

