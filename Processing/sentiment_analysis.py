from wordcloud import WordCloud, STOPWORDS
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import accuracy_score
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
import os.path
import pandas as pd

from Data_Gathering.twitter_data import get_corona_tweets


class Classifier:
    def __init__(self):
        self.classifier, self.tokenizer = self.__fit_classifier()

    def __fit_classifier(self):
        stopwords = set(STOPWORDS)
        tokenizer = CountVectorizer(stop_words=stopwords, strip_accents='ascii', ngram_range=(1, 2), max_features=5000,
                                    min_df=2)
        data = self.__read_training_data()
        y = data["label"]
        #tokenizer.set_params(max_features=5000)

        X = tokenizer.fit_transform(data['text'])
        X_train, X_test, y_train, y_test = train_test_split(X, y)
        X_train2, X_val, y_train2, y_val = train_test_split(X_train, y_train)

        clf = BernoulliNB()
        clf.fit(X_train2, y_train2)
        print(f'BernoulliNB accuracy: {accuracy_score(y_val, clf.predict(X_val))}')
        return clf, tokenizer

    def __read_training_data(self):
        if not os.path.isfile("../Data/train.csv"):
            # https://svaderia.github.io/articles/downloading-and-unzipping-a-zipfile/
            zip_url = "https://www.dropbox.com/s/octyjwtn4gwv7gm/data.zip?dl=1"
            with urlopen(zip_url) as zip_resp:
                with ZipFile(BytesIO(zip_resp.read())) as z_file:
                    z_file.extractall('../Data')

        return pd.read_csv('../Data/train.csv', sep=',', header=0)

    def get_sentiment(self, tweet_texts):
        X = self.tokenizer.transform(tweet_texts)
        predictions = self.classifier.predict(X)
        return predictions

"""
all_tweets = get_corona_tweets()
clf = Classifier()
all_tweets['sentiment'] = pd.Series(clf.get_sentiment(all_tweets['cleaned_text']), index=all_tweets.index)
print(all_tweets.iloc[0:10, [2, 4]])
"""