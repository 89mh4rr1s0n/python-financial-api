from pprint import pprint
import requests
import psycopg2
import psycopg2.extras
import yahooquery
from yahooquery import Ticker
import json
from datetime import datetime

import pymongo
mongo_uri = "mongodb://localhost:27017"
client = pymongo.MongoClient(mongo_uri) 
db = client["financialModellingPrepDB"]
collection = db["itpmData2"]

# Connect to an existing database
conn = psycopg2.connect("dbname=financialmodellingprep user=postgres password=Fastman12")

# Open a cursor to perform database operations
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

work_mem = 2048
cur.execute('SET work_mem TO %s', (work_mem,))
cur.execute('SHOW work_mem')

cur.execute("""select
	symbol,
	companyname,
	mktcap::float,
	isadr,
	isetf
from profiles
where isetf = 'false' and mktcap::float > 1000000000
order by mktcap::float asc""")

records = cur.fetchall()

def insert_recommendation_trend(ticker):
    try:
        # item = Ticker(ticker)
        item = Ticker(ticker)
        # pprint(item.recommendation_trend)
        recommendation_trend = json.loads(item.recommendation_trend.to_json(orient='records', date_format='iso'))
        # recommendation_trend.append(datetime.today().strftime("%d/%m/%Y"))
        item = {
            "updatedAt": datetime.today().strftime("%d/%m/%Y"),
            "recommendationTrend": recommendation_trend
        }
        # print(recommendation_trend)
        collection.find_one_and_update({"symbol": ticker}, { "$set": { "recommendationTrend": item }}, upsert=True)
        # print(len(item.earnings_trend[ticker]['trend']))
    except:
        # collection.find_one_and_update({"symbol": ticker}, { "$unset": { "yahooEstimates": "" }}, upsert=True)
        print('no analyst recommendations')


for rec in records:
    insert_recommendation_trend(rec[0])
    print(rec[0])