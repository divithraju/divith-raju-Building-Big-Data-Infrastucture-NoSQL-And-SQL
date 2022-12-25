# Yahoo Parser

# Parses Data and uploads to MongoDB 

import mongo_access
import yfinance as yf
import json
from pymongo import MongoClient
import os
import pandas as pd

# Connect to MongoDB
client_mongo = MongoClient(mongo_access.URL)
db_mongo = client_mongo.get_database("alikhanlab-twitter")
stocks = db_mongo.stocks

# Get data from Yahoo Finance
def parse_yahoo_and_populate(ticker, period):
    ticker = 'UBER'
    uber_stock = yf.Ticker(ticker)
    uber_df = uber_stock.history(period='1y')
    uber_json = uber_df.to_json(orient='table')
    uber_json = json.loads(uber_json)
    uber_json = uber_json['data']

    for day in uber_json:
        day['track'] = ticker
        stocks.insert_one(day)




