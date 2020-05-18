from flask import Flask, render_template, jsonify, send_from_directory
import pandas as pd

from application import Application

app = Flask(__name__)
corona_app = Application()


@app.route("/")
def home():
    return render_template("index.html")


# Routes for infections/death
@app.route('/corona', methods=["GET"])
@app.route('/corona/', methods=["GET"])
@app.route('/corona/<county>', methods=["GET"])
def infections(county=None):
    corona_data = corona_app.get_corona_data()
    if county is None:
        response = df_to_dict(corona_data)
    else:
        response = df_to_dict(corona_data[corona_data.county == county])
    return jsonify(response), 200


@app.route('/Data/<path:path>')
def send_file(path):
    return send_from_directory('../Data', path)

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
