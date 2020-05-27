from datetime import datetime
import os
from time import sleep

from logzero import logger
from Data.punct import Punct
from Data.twitter_handles import handles, corona_terms
import csv
import re
import pandas as pd


class TwitterData:
    def __init__(self, api, wd, handle=handles["Donald Trump"]):
        self.api = api
        self.wd = wd
        self.handle = handle
        self.file_name = f'{self.handle}.csv'
        self.path = f'{self.wd}/Data/Tweets/{self.file_name}'

        # Check if new tweets are available
        self.update_tweets()
        self.all_tweets = self.__read_all_tweets()
        self.all_tweets["date"] = self.all_tweets["created_at"].apply(lambda d: datetime.strptime(d, '%Y-%m-%d %H:%M:%S'))

        # Import all tweets related to the corona virus
        self.corona_tweets = self.__read_corona_tweets()
        self.corona_tweets["date"] = self.corona_tweets["created_at"].apply(
            lambda d: datetime.strptime(d, '%Y-%m-%d %H:%M:%S'))
        self.file_size = os.stat(self.path).st_size
        self.start_date = "2020-02-01"
        self.end_date = self.__get_end_date()
        logger.info("Loaded stored tweets")

    # Download all tweets which are more recent than the newest one stored in the Data Folder.
    # Updates the respective file after download
    def update_tweets(self):
        if not os.path.isfile(self.path):
            self.download_tweets()
            return

        df = pd.read_csv(self.path)
        newest = df.iloc[0].id
        all_tweets = []

        new_tweets = self.api.user_timeline(screen_name=self.handle, count=200, exclude_replies=True,
                                            include_rts=False, tweet_mode="extended", since_id=newest)
        if len(new_tweets) == 0:
            logger.info("No new tweets found")
            return

        all_tweets.extend(new_tweets)
        newest = all_tweets[0].id + 1

        while len(new_tweets) > 0:
            new_tweets = self.api.user_timeline(screen_name=self.handle, count=200, exclude_replies=True,
                                                include_rts=False, tweet_mode="extended", since_id=newest)
            all_tweets.extend(new_tweets)
            newest = all_tweets[0].id + 1
            logger.info(f"...{len(all_tweets)} tweets downloaded so far")

        out_tweets = [[tweet.id_str, tweet.created_at, tweet.full_text.encode("utf-8")] for tweet in all_tweets]
        df_out_tweets = pd.DataFrame(out_tweets, columns=["id", "created_at", "full_text"])
        df = pd.concat([df_out_tweets, df])
        if os.path.isfile(self.path):
            os.remove(self.path)
        df.to_csv(self.path, index=False)
        self.file_size = os.stat(self.path).st_size
        self.end_date = df.iloc[0]["created_at"].strftime('%Y-%m-%d')
        return df

    # Download latest ~2000 Tweets from Donald Trump and store them in the data folder
    def download_tweets(self):
        all_tweets = []

        new_tweets = self.api.user_timeline(screen_name=self.handle, count=200, exclude_replies=True,
                                            include_rts=False, tweet_mode="extended")
        if len(new_tweets) == 0:
            logger.debug("No new tweets received. API Limit may be reached")
            return
        all_tweets.extend(new_tweets)
        oldest = all_tweets[-1].id - 1
        logger.info(f"Downloading all Tweets from {self.handle}")
        while len(new_tweets) > 0:
            # Trying to avoid bumping into rate limit
            sleep(2)
            new_tweets = self.api.user_timeline(screen_name=self.handle, count=200, max_id=oldest,
                                                exclude_replies=True, include_rts=False, tweet_mode="extended")
            all_tweets.extend(new_tweets)
            oldest = all_tweets[-1].id - 1
            logger.info(f"...{len(all_tweets)} tweets downloaded so far")

        out_tweets = [[tweet.id_str, tweet.created_at, tweet.full_text.encode("utf-8")] for tweet in all_tweets]
        df = pd.DataFrame(out_tweets, columns=["id", "created_at", "full_text"])
        if os.path.isfile(self.path):
            os.remove(self.path)
        df.to_csv(self.path, index=False)
        self.file_size = os.stat(self.path).st_size
        self.end_date = self.__get_end_date()
        logger.info("Tweets downloaded!")
        return df

    # Removes unnecessary characters from string
    def __clean_text(self, text):
        cleaned_text = text.lower()
        cleaned_text = re.sub(r'\\xe2\\x80\\x\S\S', '', cleaned_text)
        cleaned_text = re.sub(r'^[\'\"]?b', '', cleaned_text)
        cleaned_text = re.sub(r'@[A-Za-z0–9]+', '', cleaned_text)  # Removing @mentions
        cleaned_text = re.sub(r'https?://\S+', '', cleaned_text)  # Removing hyperlink
        cleaned_text = re.sub(r'\d+', '0', cleaned_text)
        punct = Punct().get_punct()
        for pun in punct:
            cleaned_text = cleaned_text.replace(pun, "")
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        cleaned_text.strip()
        return cleaned_text

    # Read all tweets stored in the data folder and return it as pd.DataFrame
    def __read_all_tweets(self):
        file_path = f'{self.wd}/Data/Tweets/{self.handle}.csv'
        if not os.path.isfile(file_path):
            self.download_tweets()
        df = pd.read_csv(file_path)
        df['cleaned_text'] = df.apply(lambda row: self.__clean_text(row['full_text']), axis=1)
        return df

    # Read corona tweets stored in the data folder and return it as pd.DataFrame
    def __read_corona_tweets(self):
        df = self.__read_all_tweets()
        pattern = '|'.join(corona_terms)
        df['cleaned_text'] = df.apply(lambda row: self.__clean_text(row['full_text']), axis=1)
        df = df[df.cleaned_text.str.contains(pattern)]
        return df

    def __get_end_date(self):
        return self.all_tweets.iloc[0]["created_at"][0:10]
