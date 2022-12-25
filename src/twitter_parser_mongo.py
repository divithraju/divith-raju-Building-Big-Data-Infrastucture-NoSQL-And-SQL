# Twitter Parser

# Parses Data and uploads to MongoDB 

import twitter_access
import mongo_access
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import re
import tweepy
import time
from datetime import datetime
from dateutil.parser import parse
from pymongo import MongoClient
import os
import psycopg2
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

# Connect to MongoDB
client_mongo = MongoClient(mongo_access.URL)
db_mongo = client_mongo.get_database("alikhanlab-twitter")
tweets_mongo = db_mongo.tweets


# Twitter Parser Class
class Output_Listener(StreamListener):
    
    def __init__(self, sec_limit, track):
        self.start_time = time.time()
        self.sec_limit = sec_limit
        self.track = track
        self.analyser = SentimentIntensityAnalyzer()
        self.cities = pd.read_excel('CitiesEnriched.xls')
        
    def on_data(self, data):

        def clean_tweet(x):
            x = x.encode('ascii', 'ignore').decode('ascii')
            x = re.sub(r'http\S+', '', x)
            return x

        if (time.time() - self.start_time) < self.sec_limit:
            tweet = json.loads(data)
            if tweet["retweeted"] == False:
                created_at = parse(tweet["created_at"])
                tweet_id_str = tweet["id_str"]
                text = clean_tweet(tweet["text"])
                retweet_count = tweet["retweet_count"]
                favorite_count = tweet["favorite_count"]
                user_id = tweet["user"]["id_str"]
                user_followers_count = tweet["user"]["followers_count"]
                # text sentiment
                tweet_sentiment = self.analyser.polarity_scores(text)

                # user geolocation
                city = self.cities.sample()
                longitude = city['Lng'].values[0]
                latitude = city['Lat'].values[0]

                obj = {"track":self.track[0],"created_at":created_at,"tweet_id_str":tweet_id_str,"text":text,
                      "neg_score":tweet_sentiment["neg"],
                      "neu_score":tweet_sentiment["neu"],
                      "pos_score":tweet_sentiment["pos"],
                      "retweet_count":retweet_count,
                      "favorite_count":favorite_count, "user_id":user_id, "user_followers_count":user_followers_count,
                      "user_long": longitude, "user_lat":latitude}

                tweets_mongo.insert_one(obj)
                print('Tweet is uploaded on MongoDB')
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
    


