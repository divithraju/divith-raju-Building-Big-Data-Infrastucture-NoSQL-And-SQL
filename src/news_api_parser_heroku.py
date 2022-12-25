# Parse News API to Heroku(Cloud PostgreSQL)

import heroku_access
import news_access
import os
import psycopg2
from newsapi import NewsApiClient


# Conenct to Heroku
conn = psycopg2.connect(
        host = heroku_access.host,
        database = heroku_access.database,
        user = heroku_access.user,
        password = heroku_access.password)

# cursor
cur = conn.cursor()

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
        source_id = article['source']['id']
        source_name = article['source']['name']
        author = article['author']
        title = article['title']
        description = article['description']
        url = article['url']
        url_image = article['urlToImage']
        published_at = article['publishedAt']
        content_ = article['content']
        track = article['track']
        parse_list = [source_id, source_name, author, title, description, url, url_image, published_at, content_, track]
        parse_list = ['None' if x==None else x for x in parse_list]
        parse_list = [x.replace("'",'') for x in parse_list]
        parse_list = [repr(x) for x in parse_list]
        insert_query = "INSERT INTO articles VALUES({},{},{},{},{},{},{},{},{},{});".format(*parse_list)
        cur.execute(insert_query)
        cur.commit()


