# Yahoo Parser

# Parses Data and uploads to MongoDB and Heroku

import heroku_access
import re
import os
import psycopg2
import yfinance as yf
import json

# Conenct to Heroku
conn = psycopg2.connect(
        host = heroku_access.host,
        database = heroku_access.database,
        user = heroku_access.user,
        password = heroku_access.password)

# cursor
cur = conn.cursor()

def parse_yahoo_and_populate(ticker, period):
    ticker = 'UBER'
    uber_stock = yf.Ticker(ticker)
    uber_df = uber_stock.history(period='1y')
    uber_json = uber_df.to_json(orient='table')
    uber_json = json.loads(uber_json)
    uber_json = uber_json['data']

    for day in uber_json:
        parse_list = list(day.values())
        parse_list[0] = repr(parse_list[0])
        parse_list.append(repr(ticker))
        insert_query = "INSERT INTO stocks VALUES({},{},{},{},{},{},{},{},{});".format(*parse_list)
        cur.execute(insert_query)
        conn.commit()

