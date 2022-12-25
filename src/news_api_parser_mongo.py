# Parse News API to MongoDB

from pymongo import MongoClient
from newsapi import NewsApiClient
import requests
import json
import mongo_access
import news_access

# Connect to MongoDB
client_mongo = MongoClient(mongo_access.URL)
db_mongo = client_mongo.get_database("alikhanlab-twitter")
articles = db_mongo.articles

# News API
newsapi = NewsApiClient(api_key=news_access.api_key)

def parse_and_populate_news(from_date, to_date, page_size, track):
    from_date = '2020-04-20'
    to_date = '2020-04-27'
    page_size = 100
    track = 'Starbucks'
    all_articles = newsapi.get_everything(q=track,
                                        from_param=from_date,
                                        to=to_date,
                                        language='en',
                                        page_size = page_size)
    for article in all_articles['articles']:
        article['track'] = track
        articles.insert_one(article)

