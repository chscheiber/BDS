from flask import Flask, render_template, jsonify
import pandas as pd

from Data_Gathering.corona_data import CoronaData
from Data_Gathering.twitter_data import get_corona_tweets
from Processing.sentiment_analysis import Classifier
from init import InitApplication

app = Flask(__name__)
corona_data = CoronaData().read_data()
corona_app = InitApplication()

@app.route("/")
def home():
    return render_template("index.html")


# Routes for infections/death
@app.route('/corona_data', methods=["GET"])
@app.route('/corona_data/', methods=["GET"])
@app.route('/corona_data/<state>', methods=["GET"])
def infections(state=None):
    if state is None:
        response = df_to_dict(corona_data)
    else:
        response = df_to_dict(corona_data[corona_data.state == state])
    return jsonify(response), 200


# Routes for Tweets
@app.route('/corona_tweets', methods=["GET"])
def corona_tweets():
    all_tweets = corona_app.create_tweet_data()
    # Convert Dataframe to jsonifyable dict
    return jsonify(df_to_dict(all_tweets)), 200


def df_to_dict(df):
    result = {}
    for index, row in df.iterrows():
        result[index] = dict(row)
    return result
