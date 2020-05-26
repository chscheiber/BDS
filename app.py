from datetime import datetime
from flask import Flask, render_template, jsonify, send_from_directory

from data_interface import Application

"""
Init Flask app and Backend
"""
corona_app = Application()
template_dir = f"{corona_app.wd}/Frontend/templates"
static_dir = f"{corona_app.wd}/Frontend/static"
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)


"""
-------------------------------------
Routes for HTML Templates
-------------------------------------
"""


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


"""
-------------------------------------
Routes for corona  data
-------------------------------------
"""


# Get corona data in general or for specific county for all available dates
@app.route('/corona', methods=["GET"])
@app.route('/corona/', methods=["GET"])
@app.route('/corona/<county>', methods=["GET"])
@app.route('/corona/<county>/<date>', methods=["GET"])
def infections(county=None, date=None):
    corona_data = corona_app.get_all_corona_data()
    if county is None:
        response = df_to_dict(corona_data)
    elif date is not None:
        df = corona_app.get_corona_data_per_date(date)
        response = df_to_dict(df[df.county == county])
    else:
        response = df_to_dict(corona_data[corona_data.county == county])
    return jsonify(response), 200


# Get corona data for all counties for a specified date
@app.route('/corona_date/<date>')
def corona_per_date(date=corona_app.cd.end_date):
    # TODO Change to list
    corona_data = corona_app.get_corona_data_per_date(date)
    return jsonify(df_to_dict(corona_data)), 200


# Returns all cases and deaths aggregated per county from the start date up to the specified date
@app.route('/aggregated/<date>')
def aggregated(date=corona_app.cd.end_date):
    data = corona_app.get_aggregated_corona_data(date)
    return jsonify(cases=int(data["cases"]),
                   deaths=int(data["deaths"])), 200


"""
-------------------------------------
Routes for Static Data/ Data for Visualization
-------------------------------------
"""


# Get all US counties
@app.route('/counties')
def counties():
    all_counties = corona_app.counties
    return jsonify(df_to_dict(all_counties))


# Get static files in Data folder
@app.route('/Data/<path:path>')
def send_file(path):
    return send_from_directory('../Data', path)


"""
-------------------------------------
Routes for Tweets
-------------------------------------
"""


# Get all tweets containing corona terms up to the specified date
@app.route('/corona_tweets/<date>', methods=["GET"])
def corona_tweets(date=corona_app.cd.start_date):
    return __transform_tweets(corona_app.get_tweets_before(date, corona_app.corona_tweets)), 200


# Get all tweets up to the specified date
@app.route('/all_tweets/<date>', methods=["GET"])
def all_tweets(date=corona_app.cd.start_date):
    return __transform_tweets(corona_app.get_tweets_before(date, corona_app.all_tweets)), 200


"""
-------------------------------------
Routes for JS Scripts
-------------------------------------
"""


# Get start date for viz
@app.route('/start_date')
def start_date():
    return jsonify(date=corona_app.cd.start_date), 200


# Get end date for viz
@app.route('/end_date')
def end_date():
    return jsonify(date=corona_app.cd.end_date), 200


# Get only cases up to specified date
@app.route('/cases_until/<date>')
def cases_until(date=corona_app.cd.start_date):
    return jsonify(cases=(int(date[0:4]) + int(date[8:10]))), 200


# Get only deaths up to specified date
@app.route('/deaths_until/<date>')
def deaths_until(date=corona_app.cd.start_date):
    return jsonify(deaths=date[8:10]), 200


"""
-------------------------------------
Admin Routes
-------------------------------------
"""


@app.route('/corona_file_data')
def corona_file_data():
    return jsonify(file_name=corona_app.cd.file_name,
                   file_size=corona_app.cd.file_size,
                   start_date=corona_app.cd.start_date,
                   end_date=corona_app.cd.end_date), 200


@app.route('/twitter_file_data')
def twitter_file_data():
    return jsonify(file_name=corona_app.td.file_name,
                   file_size=corona_app.td.file_size,
                   start_date=corona_app.td.start_date,
                   end_date=corona_app.td.end_date), 200


@app.route('/update_corona_data')
def update_corona_data():
    corona_app.cd.download_data()
    return corona_file_data()


@app.route('/update_twitter_data')
def update_twitter_data():
    corona_app.td.update_tweets()
    return twitter_file_data()


"""
-------------------------------------
Helper functions
-------------------------------------
"""


# Convert DataFrame to dictionary
def df_to_dict(df):
    result = {}
    for index, row in df.iterrows():
        result[index] = dict(row)
    return result


def __transform_tweets(tweets):
    # Reverse Dataframe
    tweets = tweets.iloc[::-1]
    tweets["date"] = tweets["date"].apply(lambda d: datetime.strftime(d, '%Y-%m-%d'))
    tweet_polarity = tweets.groupby(["date"])["Polarity"].mean().to_list()
    tweet_subjectivity = tweets.groupby(["date"])["Subjectivity"].mean().to_list()
    tweet_text = tweets["full_text"].to_list()
    tweet_date = tweets["date"].to_list()
    return jsonify(date=tweet_date,
                   text=tweet_text,
                   subjectivity=tweet_subjectivity,
                   polarity=tweet_polarity)


if __name__ == '__main__':
    app.run()
