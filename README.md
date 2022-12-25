# Building-Big-Data-Infrastucture-using-NoSQL-and-SQL
Big Data Pltaform on MongoDB Atlas and Heroku PostgreSQL

## Background

The motivation behind this project is I see a lot of big data datasets on the internet, people used for data analysis and machine learning, so this time I am interested to build what is behind these big datasets and how to build big data infrastructure. 

## Methodology

- First, finding Developer API’s for enriching the database. I found Tweeter API, Yahoo Finance API, and News API all three API’s are available with registration.   
- Then, writing Python codes to connect to Databases and consuming data using API’s and populating both NoSQL and SQL databases.
- Last, building dashboards and connecting to Databricks.

![methodology](/assets/data_pipeline.png)

## Tech Stack and Implementation

Almost the same code used for parsing data from Twitter, Yahoo, News API for NoSQL and SQL Databases the difference was only in connecting populating databases. For parsing data from twitter used Python ‘tweepy’ package, and it also provides some code snippets to start with.

For NoSQL big data infrastructure, I used MongoDB Atlas free cluster that provides 500 connections per day and 512 mb of free database size. Consuming data from Twitter, Yahoo, News API I used Python, also connecting to database MongoDB Python API Client. Before populating database, I created 3 collections (tweets, articles, stocks) using MongoDB atlas, no DDL needed. MongoDB documentation is clear and easy to use.

Python connector to MongoDB using Python ‘pymongo’ package, where we authenticate and we have access to the database.
Connecting Databricks Community Version free cluster and MongoDB Atlas used MongoDB Spark Connector.
MongoDB charts used for building real-time dashboards, connected to your MongoDB Atlas and automatically updates charts once we insert data into database.

For SQL database, I decided to go with PostgreSQL because it is open source and it would be easier in the feature if there is a need to transfer data from one platform to another. Also, there are many option on using PostgreSQL on cloud, then SQL Server or Oracle. Searching free and potentially easy to scale PostgreSQL platform I left my choice to Heroku PostgreSQL, which provides a wide range of features like testing schema migration, manage database access levels and protect queries, scale horizontally and quick access of data.

Python connector to Heroku PostgreSQL. Basically, for all PostgreSQL database there is a Python connector called ‘psycopg2’.
Also, we can access PostgreSQL database using PgAdmin as like it is local PostgreSQL.

## Dependencies

- Python packages
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install python dependencies.
```bash
pip install -r requirements.txt
```
- Twitter API Access. Get Developer API token from [here](https://developer.twitter.com/en/apply-for-access)
- News API Access. Get Developer API token from [here](https://newsapi.org/)
- Yahoo Finance API. Get access [here](https://pypi.org/project/yahoo-finance/)

- Databases:
  - MongoDB Atlas. Get Free 512MB cloud cluster [here](https://www.mongodb.com/cloud/atlas)
  - Heroku PostgreSQL. Get cloud database for non-comercial apps [here](https://www.mongodb.com/cloud/atlas)

## License

Licensed under the [MIT License](LICENSE.txt) 
