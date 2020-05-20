# Final BDS Project Project_ 33

## About our Project
The goal of our BDS Project is to answer the following research question:
"How is the sentiment of Donald Trump's tweets influenced by the spread of the corona virus in the United States?"

## CEO Perspective
To provide a high level overview about the research question we decided to generate a D3js Dashboard
to visualize the spread of the corona virus in the United States over time in comparison
to Donald Trump's opinion on the corona virus. The opinion of Donald Trump is calculated using a
sentiment analysis on a subset of his tweets. This subset contains all tweets issued by him which
contain at least one predefined term related to the Covid-19 pandemic.

## Data Engineer 
To create a reusable app all the data we are using is provided via a REST API. 
This data is generated by an ETL-Pipeline which queries, transforms and provides Donald Trumps tweets and up-to-date
data concerning the corona virus issued by de NY Times.

## Implementation
For the implementation of our project we are using a Full Stack approach with Python running in the backend
and a JavaScript Frontend. The Visualizations were created with D3js, the styling is done via bootstrap.

## Running the demo
1. Install requirements using: pip install -r requirements.txt
2. Add an .env file in the same folder as app.py 
3. Run app.py to start a Flask Server
4. Open localhost:5000 in Browser
---
.env:<br>
consumer_key = <consumer_key><br>
consumer_secret = <consumer_secret><br>
access_token = <access_token><br>
access_token_secret = <access_token_secret><br>

## API
Our API offers the following routes:

/corona
- Returns all cases and deaths for all counties and all dates

/corona/\<county>
- Returns all cases and deaths for all dates in the specified county

/corona_date/\<date>
- Returns all cases and deaths for all counties on the specified date

/aggregated/\<date>
- Returns all cases and deaths for all counties aggregated on the specified

/corona_tweets/\<date>
- Returns all tweets containing corona terms up to the specified date

/all_tweets/\<date>
- Returns all tweets up to the specified date

/cases_until/\<date>
- Returns amount of cases up to specified date

/deaths_until/\<date>
- Returns amount of deaths up to specified date

/start_date
- Returns the start date for viz

/end_date
- Returns the end date for viz

/kpis/\<date>
- Returns cases and deaths up to specified date

/counties
- Returns all US counties

/Data/\<path>
- Returns static files in Data folder

## Status
![D3](/img/status_1805.png)