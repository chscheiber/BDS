import random
from datetime import datetime
from flask import Flask, render_template, jsonify, send_from_directory
import pandas as pd

from application import Application

app = Flask(__name__)
corona_app = Application()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


# Routes for infections/death
@app.route('/corona', methods=["GET"])
@app.route('/corona/', methods=["GET"])
@app.route('/corona/<county>', methods=["GET"])
def infections(county=None):
    corona_data = corona_app.get_all_corona_data()
    if county is None:
        response = df_to_dict(corona_data)
    else:
        response = df_to_dict(corona_data[corona_data.county == county])
    return jsonify(response), 200


@app.route('/corona_date/<date>')
def corona_per_date(date="2020-05-15"):
    #TODO Change to list
    corona_data = corona_app.get_corona_data_per_date(date)
    return jsonify(df_to_dict(corona_data)), 200


@app.route('/counties')
def counties():
    all_counties = corona_app.counties
    return jsonify(df_to_dict(all_counties))


@app.route('/Data/<path:path>')
def send_file(path):
    return send_from_directory('../Data', path)


# Routes for Tweets
@app.route('/corona_tweets/<date>', methods=["GET"])
def corona_tweets(date=corona_app.start_date):
    all_tweets_reverse = corona_app.get_tweets_before(date)
    all_tweets = all_tweets_reverse.iloc[::-1]
    tweet_text = all_tweets["full_text"].to_list()
    tweet_date = all_tweets["date"].apply(lambda d: datetime.strftime(d, '%Y-%m-%d')).to_list()
    tweet_subjectivity = all_tweets["Subjectivity"].to_list()
    tweet_polarity = all_tweets["Polarity"].to_list()
    return jsonify(date=tweet_date,
                   text=tweet_text,
                   subjectivity=tweet_subjectivity,
                   polarity=tweet_polarity), 200


# Routes for JS Scripts
@app.route('/start_date')
def start_date():
    return jsonify(date=corona_app.start_date), 200


@app.route('/end_date')
def end_date():
    return jsonify(date=corona_app.end_date), 200


@app.route('/kpis/<date>')
def kpis(date=corona_app.start_date):
    return jsonify(cases=(int(date[0:4])+int(date[8:10])),
                   deaths=date[8:10]), 200


@app.route('/cases_until/<date>')
def cases_until(date=corona_app.start_date):
    return jsonify(cases=(int(date[0:4])+int(date[8:10]))), 200


@app.route('/deaths_until/<date>')
def deaths_until(date=corona_app.start_date):
    return jsonify(deaths=date[8:10]), 200


@app.route('/sentiment/<date>')
def sentiment(date=corona_app.start_date):
    return jsonify(sentiment=random.random()), 200


@app.route('/test_list')
def test_list():
    return jsonify(data_list=[1, 2, 3, 4, 5])


def df_to_dict(df):
    result = {}
    for index, row in df.iterrows():
        result[index] = dict(row)
    return result


if __name__ == '__main__':
    app.run()
