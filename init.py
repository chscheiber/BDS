import pandas as pd
import tweepy
import os
from Data_Gathering.twitter_data import get_corona_tweets
from Processing.sentiment_analysis import Classifier
from env_gitignore import consumer_key, consumer_secret, access_token, access_token_secret


class InitApplication:
    def __init__(self):
        self.api = self.init_tweepy_api()
        self.classifier = Classifier()

    def init_tweepy_api(self):
        # Consumer keys and access tokens, used for OAuth
        from Frontend.api import app

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

