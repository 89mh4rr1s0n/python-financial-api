import json
from urllib import response
import investpy
import datetime
import requests
import psycopg2
import psycopg2.extras
import pprint
import yfinance as yf
import json

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

def insert_press_releases(ticker):


    releases = requests.get('https://financialmodelingprep.com/api/v3/press-releases/' + ticker + '?apikey=e812649ac124bbb4d773e2ff24a28f0d')

    check = collection.count_documents({'symbol': ticker})

    print(len(releases.json()))

    if check == 0:
        collection.insert_one({
            'symbol': ticker,
            'pressReleases': releases.json(),
            'noOfReleases': len(releases.json())
        })
    elif check == 1:
        collection.find_one_and_update({'symbol': ticker},{"$set": {'pressReleases': releases.json(), 'noOfReleases': len(releases.json())}})


def insert_analyst_estimates(ticker):
    try:
        item = yf.Ticker(ticker)
        response = json.loads(item.analysis.to_json(orient='records', date_format='iso'))
        collection.find_one_and_update({"symbol": ticker}, { "$set": { "yahooEstimates": response }}, upsert=True)
    except:
        print('no estimates for this symbol')

for rec in records[120:]:
    insert_analyst_estimates(rec[0])
    # insert_press_releases(rec[0])
    print(rec[0])