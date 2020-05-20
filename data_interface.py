import pandas as pd
import tweepy
import os
from datetime import datetime
from dotenv import load_dotenv

from Data_Gathering.corona_data import CoronaData
from Data_Gathering.twitter_data import TwitterData
from Processing.sentiment_analysis import Classifier


"""
Main Application that serves as communication between Flask API and Data Gathering
"""


class Application:
    def __init__(self):
        load_dotenv()
        self.api = self.__init_tweepy_api()
        self.classifier = Classifier()
        self.wd = os.path.dirname(__file__)

        # Loading corona data based on NY-Times sourcce
        self.cd = CoronaData(self.wd)
        self.start_date = "2020-02-01"
        self.end_date = self.cd.end_date
        self.counties = self.__read_counties()

        # Loading Tweets from Donald Trump
        self.td = TwitterData(self.api, self.wd)
        self.corona_tweets = self.__get_tweets_with_sentiment(self.td.corona_tweets)
        self.all_tweets = self.__get_tweets_with_sentiment(self.td.all_tweets)

    def __init_tweepy_api(self):
        # Consumer keys and access tokens, used for OAuth
        consumer_key = os.getenv("consumer_key")
        consumer_secret = os.getenv("consumer_secret")
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        access_token = os.getenv("access_token")
        access_token_secret = os.getenv("access_token_secret")
        auth.set_access_token(access_token, access_token_secret)
        # Calling the api
        return tweepy.API(auth, wait_on_rate_limit_notify=True, wait_on_rate_limit=True)

    # Takes df as input and adds polarity and subjectivity columns
    def __get_tweets_with_sentiment(self, tweets):
        clf = Classifier()
        tweets = clf.get_classified_df(tweets)
        return tweets

    # Filter tweets to only return tweets tweeted before the given date
    def get_tweets_before(self, date, tweets):
        date = datetime.strptime(date, '%Y-%m-%d')
        tweets_before_date = tweets[tweets["date"] <= date]
        return tweets_before_date

    # Returns the whole corona dataset as pd.DataFrame
    def get_all_corona_data(self):
        corona_data = self.cd.data
        return corona_data

    # Returns pd.DataFrame with cases and deaths per county on the respective date
    def get_corona_data_per_date(self, date):
        corona_data = self.cd.data
        corona_data = corona_data[corona_data.date == date]
        return corona_data

    # Sums cases and deaths of all counties per date
    def get_aggregated_corona_data(self, date):
        corona_data = self.get_corona_data_per_date(date)
        cases = corona_data["cases"].sum()
        deaths = corona_data["deaths"].sum()
        return {"cases": cases, "deaths": deaths}

    # Loads Counties and returns them as pd.DataFrame for Visualization
    def __read_counties(self):
        file_path = f"{self.wd}/Data/fips_counties.csv"
        df = pd.read_csv(file_path)
        return df



"""
application = Application()
print(application.get_corona_data_per_date("2020-02-15"))
print(application.get_counties())


application = Application()
all_tweets = application.get_tweets_before("2020-04-01")
tweet_text = all_tweets["full_text"]
tweet_date = all_tweets["date"].apply(lambda d: datetime.strftime(d, '%Y-%m-%d'))
tweet_subjectivity = all_tweets["Subjectivity"]
tweet_polarity = all_tweets["Polarity"]

print({
    "date": tweet_date,
    "text": tweet_text,
    "subjectivity": tweet_sentiment,
    "polarity": tweet_polarity
})

application = Application()
application.get_aggregated_corona_data("2020-05-14")
"""
