from flask import Flask, render_template, jsonify
import pandas as pd

from Data_Gathering.corona_data import CoronaData
from Data_Gathering.twitter_data import get_corona_tweets
from Processing.sentiment_analysis import Classifier
from init import InitApplication

app = Flask(__name__)
corona_data = CoronaData().get_corona_data()
corona_app = InitApplication()

@app.route("/")
def home():
    return render_template("index.html")


# Routes for infections/death
@app.route('/<data>', methods=["GET"])
@app.route('/<data>/', methods=["GET"])
@app.route('/<data>/<region>', methods=["GET"])
def infections(data, region=None):
    response = None
    if data not in corona_data.keys():
        return "Page not found", 404

    infections_data = corona_data[data]
    if region is None or region is "" or region not in infections_data.keys():
        # Convert Dataframe to jsonifyable dict
        tmp = {}
        for key, df in infections_data.items():
            tmp_row = {}
            for index, row in df.iterrows():
                tmp_row[index] = dict(row)
            tmp[key] = tmp_row
        response = tmp
    else:
        # Convert Dataframe to jsonifyable dict
        tmp = {}
        for index, row in infections_data[region].iterrows():
            tmp[index] = dict(row)
        response = tmp

    return jsonify(response), 200


# Routes for Tweets
@app.route('/corona_tweets', methods=["GET"])
def corona_tweets():
    all_tweets = corona_app.create_tweet_data()
    # Convert Dataframe to jsonifyable dict
    result = {}
    for index, row in all_tweets.iterrows():
        result[index] = dict(row)
    return jsonify(result), 200

