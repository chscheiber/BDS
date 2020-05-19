import os
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
        self.all_tweets = self.__read_all_tweets()
        self.corona_tweets = self.__read_corona_tweets()

    def create_tweet_files(self):
        all_tweets = []
        new_tweets = self.api.user_timeline(screen_name=self.handle, count=200, exclude_replies=True, include_rts=False,
                                            tweet_mode="extended")
        if len(new_tweets) == 0:
            logger.debug("No new tweets received. API Limit may be reached")
            return
        all_tweets.extend(new_tweets)

        oldest = all_tweets[-1].id - 1

        while len(new_tweets) > 0:
            new_tweets = self.api.user_timeline(screen_name=self.handle, count=200, max_id=oldest,
                                                exclude_replies=True, include_rts=False, tweet_mode="extended")
            all_tweets.extend(new_tweets)
            oldest = all_tweets[-1].id - 1
            print(f"...{len(all_tweets)} tweets downloaded so far")

        out_tweets = [[tweet.id_str, tweet.created_at, tweet.full_text.encode("utf-8")] for tweet in all_tweets]

        # write the csv
        with open(f'{self.wd}/Data/Tweets/{self.handle}.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["id", "created_at", "full_text"])
            writer.writerows(out_tweets)

    def __clean_text(self, text):
        cleaned_text = text.lower()
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

    def __read_all_tweets(self):
        file_path = f'{self.wd}/Data/Tweets/{self.handle}.csv'
        if not os.path.isfile(file_path):
            self.create_tweet_files()
        df = pd.read_csv(file_path)
        return df

    def __read_corona_tweets(self):
        file_path = f'{self.wd}/Data/Tweets/{self.handle}_corona.csv'
        if not os.path.isfile(file_path):
            df = self.__read_all_tweets()
            pattern = '|'.join(corona_terms)
            df['cleaned_text'] = df.apply(lambda row: self.__clean_text(row['full_text']), axis=1)
            df = df[df.cleaned_text.str.contains(pattern)]
            df.to_csv(file_path)
        else:
            df = pd.read_csv(file_path)
        return df

    # TODO implement "update_tweet_files"
    def update_tweet_files(self):
        pass
