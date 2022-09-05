
import pymongo
from pprint import pprint
mongo_uri = "mongodb://localhost:27017"
client = pymongo.MongoClient(mongo_uri) 
db = client["financialModellingPrepDB"]
collection = db["ismManufacturing"]
man_hist_collection = db["ismManHist"]

date = "01/06/2022"

ism_man = {
    "date": "01/06/2022",
    "value": 54
}

ism_man_doc = man_hist_collection.find({"index": "ISM_MAN"})

# print([x['date'] for x in ism_man_doc['data']])
for doc in ism_man_doc:
    dates = [x['date'] for x in doc['data']]
    pprint(dates)
    if date not in dates:
        print('insert here')
    
