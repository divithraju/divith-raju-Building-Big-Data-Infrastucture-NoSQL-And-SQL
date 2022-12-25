# Twitter Parser Heroku (Cloud PostgreSQL)

import os
import psycopg2

import twitter_access
import heroku_access
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import re
from datetime import datetime
from dateutil.parser import parse
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time


# Conenct to Heroku
conn = psycopg2.connect(
        host = heroku_access.host,
        database = heroku_access.database,
        user = heroku_access.user,
        password = heroku_access.password)

# cursor
cur = conn.cursor()

class Output_Listener(StreamListener):
    
    def __init__(self, sec_limit, track):
        self.start_time = time.time()
        self.sec_limit = sec_limit
        self.analyser = SentimentIntensityAnalyzer()
        self.track = track
        self.cities = pd.read_excel('CitiesEnriched.xls')
    
    def on_data(self, data):

        def clean_tweet(x):
            #clean tweet
            x = x.encode('ascii', 'ignore').decode('ascii')
            x = re.sub(r'http\S+', '', x)
            return x

        if (time.time() - self.start_time) < self.sec_limit:
            tweet = json.loads(data)
            if tweet["retweeted"] == False:
                created_at = repr(tweet["created_at"])
                tweet_id_str = repr(tweet["id_str"])
                text = repr(clean_tweet(tweet["text"]).replace("'",''))
                retweet_count = tweet["retweet_count"]
                favorite_count = tweet["favorite_count"]
                user_id = repr(tweet["user"]["id_str"])
                user_followers_count = tweet["user"]["followers_count"]
                # text sentiment
                tweet_sentiment = self.analyser.polarity_scores(text)
                neg_score = tweet_sentiment['neg']
                neu_score = tweet_sentiment['neu']
                pos_score = tweet_sentiment['pos']
                # user geolocation
                city = self.cities.sample()
                longitude = city['Lng'].values[0]
                latitude = city['Lat'].values[0]
                track = repr(self.track[0])
                parse_list = [track, created_at, tweet_id_str, text, neg_score, neu_score, pos_score,
                             retweet_count, favorite_count, user_id, user_followers_count, longitude, latitude]
                insert_query = "INSERT INTO tweets VALUES({},{},{},{},{},{},{},{},{},{},{},{},{});".format(*parse_list)
                cur.execute(insert_query)
                conn.commit()
                print('Tweet is uploaded on Heroku')
            return True
        else:
            print('End parsing.....')
            print('Time limit is reached')
            return False
    
    def on_error(self, status):
        print(status)
        
def parse_and_populate(sec_limit, track):
    listener = Output_Listener(sec_limit, track)
    auth = OAuthHandler(twitter_access.API_KEY, twitter_access.API_SECRET_KEY)
    auth.set_access_token(twitter_access.ACCESS_TOKEN, twitter_access.ACCESS_TOKEN_SECRET)
    stream = Stream(auth, listener)
    stream.filter(languages = ['en'], track = track)
