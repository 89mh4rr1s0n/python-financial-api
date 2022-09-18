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

def insert_earnings_trend(ticker):
    try:
        item = Ticker(ticker)
        mongo_obj = {
            "updatedAt": datetime.today().strftime("%d/%m/%Y"),
            "yahooEstimates": item.earnings_trend[ticker]['trend']
        }
        collection.find_one_and_update({"symbol": ticker}, { "$set": { "yahooEstimates": mongo_obj }}, upsert=True)
        # print(len(item.earnings_trend[ticker]['trend']))
    except:
        collection.find_one_and_update({"symbol": ticker}, { "$unset": { "yahooEstimates": "" }}, upsert=True)


for rec in records:
    insert_earnings_trend(rec[0])
    # insert_press_releases(rec[0])
    print(rec[0])