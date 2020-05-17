from Data.punct import Punct
from Data.twitter_handles import handles, corona_terms
import csv
import re
import pandas as pd


# TODO implement "update_tweet_files" (maybe chronjob?)
def update_tweet_files():
    pass


def __create_tweet_files(api):
    for handle in handles.values():
        all_tweets = []
        new_tweets = api.user_timeline(screen_name=handle, count=200, exclude_replies=True, include_rts=False)
        all_tweets.extend(new_tweets)

        oldest = all_tweets[-1].id - 1

        while len(new_tweets) > 0:
            new_tweets = api.user_timeline(screen_name=handle, count=200, max_id=oldest,
                                           exclude_replies=True, include_rts=False)
            all_tweets.extend(new_tweets)
            oldest = all_tweets[-1].id - 1
            print(f"...{len(all_tweets)} tweets downloaded so far")

        out_tweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in all_tweets]

        # write the csv
        with open(f'../Data/Tweets/{handle}.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["id", "created_at", "text"])
            writer.writerows(out_tweets)


def __clean_text(text):
    cleaned_text = text.lower()
    cleaned_text = re.sub(r'^[\'\"]?b', '', cleaned_text)
    cleaned_text = re.sub(r'@[A-Za-z0–9]+', '', cleaned_text)    # Removing @mentions
    cleaned_text = re.sub(r'https?://\S+', '', cleaned_text)   # Removing hyperlink
    cleaned_text = re.sub(r'\d+', '0', cleaned_text)
    punct = Punct().get_punct()
    for pun in punct:
        cleaned_text = cleaned_text.replace(pun, "")
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    cleaned_text.strip()
    return cleaned_text


def get_corona_tweets(base_dir='..', handle=handles["Donald Trump"]):
    file_path = f'{base_dir}/Data/Tweets/{handle}.csv'
    df = pd.read_csv(file_path)    
    pattern = '|'.join(corona_terms)
    df['cleaned_text'] = df.apply(lambda row: __clean_text(row['text']), axis=1)
    df = df[df.cleaned_text.str.contains(pattern)]
    return df
