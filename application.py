import pandas as pd
import tweepy
import os

from Data_Gathering.corona_data import CoronaData
from Data_Gathering.twitter_data import get_corona_tweets
from Processing.sentiment_analysis import Classifier
from env import consumer_key, consumer_secret, access_token, access_token_secret


class Application:
    def __init__(self):
        self.api = self.init_tweepy_api()
        self.classifier = Classifier()
        self.wd = os.path.dirname(__file__)
        self.cd = CoronaData(self.wd)
        self.start_date = "2020-02-01"
        self.end_date = self.cd.end_date
        self.counties = self.__read_counties()

    def init_tweepy_api(self):
        # Consumer keys and access tokens, used for OAuth

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        # Calling the api
        return tweepy.API(auth)

    def create_tweet_data(self):
        all_tweets = get_corona_tweets(base_dir=self.wd)
        clf = Classifier()
        all_tweets['sentiment'] = pd.Series(clf.get_sentiment(all_tweets['cleaned_text']), index=all_tweets.index)
        return all_tweets

    def get_corona_data(self):
        corona_data = self.cd.data
        return corona_data

    def get_corona_data_per_date(self, date):
        corona_data = self.cd.data
        corona_data = corona_data[corona_data.date == date]
        return corona_data

    def __read_counties(self):
        file_path = f"{self.wd}/Data/fips_counties.csv"
        df = pd.read_csv(file_path)
        return df


"""
application = Application()
print(application.get_corona_data_per_date("2020-02-15"))
print(application.get_counties())
"""