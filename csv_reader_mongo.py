import csv
import json
from datetime import datetime

import pymongo
mongo_uri = "mongodb://localhost:27017"
client = pymongo.MongoClient(mongo_uri) 
db = client["financialModellingPrepDB"]
collection = db["ismManHist"]

filenames = [
    "C:\\Users\Matthew\Downloads\PTM_v2.0\Anton_Kreil_PTM_v2.0_Video\Documents-updated\Video 07 - ism-manufacturing\csv's\csv'sISM-MAN - CopyCUSTOMER_INVENTORIES.csv",
    "C:\\Users\Matthew\Downloads\PTM_v2.0\Anton_Kreil_PTM_v2.0_Video\Documents-updated\Video 07 - ism-manufacturing\csv's\csv'sISM-MAN - CopyDELIVERIES.csv",
    "C:\\Users\Matthew\Downloads\PTM_v2.0\Anton_Kreil_PTM_v2.0_Video\Documents-updated\Video 07 - ism-manufacturing\csv's\csv'sISM-MAN - CopyEMPLOYMENT.csv",
    "C:\\Users\Matthew\Downloads\PTM_v2.0\Anton_Kreil_PTM_v2.0_Video\Documents-updated\Video 07 - ism-manufacturing\csv's\csv'sISM-MAN - CopyEXPORTS.csv",
    "C:\\Users\Matthew\Downloads\PTM_v2.0\Anton_Kreil_PTM_v2.0_Video\Documents-updated\Video 07 - ism-manufacturing\csv's\csv'sISM-MAN - CopyIMPORTS.csv",
    "C:\\Users\Matthew\Downloads\PTM_v2.0\Anton_Kreil_PTM_v2.0_Video\Documents-updated\Video 07 - ism-manufacturing\csv's\csv'sISM-MAN - CopyINVENTORIES.csv",
    "C:\\Users\Matthew\Downloads\PTM_v2.0\Anton_Kreil_PTM_v2.0_Video\Documents-updated\Video 07 - ism-manufacturing\csv's\csv'sISM-MAN - CopyISM_MAN.csv",
    "C:\\Users\Matthew\Downloads\PTM_v2.0\Anton_Kreil_PTM_v2.0_Video\Documents-updated\Video 07 - ism-manufacturing\csv's\csv'sISM-MAN - CopyNEW_ORDERS.csv",
    "C:\\Users\Matthew\Downloads\PTM_v2.0\Anton_Kreil_PTM_v2.0_Video\Documents-updated\Video 07 - ism-manufacturing\csv's\csv'sISM-MAN - CopyORDER_BACKLOG.csv",
    "C:\\Users\Matthew\Downloads\PTM_v2.0\Anton_Kreil_PTM_v2.0_Video\Documents-updated\Video 07 - ism-manufacturing\csv's\csv'sISM-MAN - CopyPRICES.csv",
    "C:\\Users\Matthew\Downloads\PTM_v2.0\Anton_Kreil_PTM_v2.0_Video\Documents-updated\Video 07 - ism-manufacturing\csv's\csv'sISM-MAN - CopyPRODUCTION.csv"
]

series_names = [
    "CUSTOMER_INVENTORIES",
    "DELIVERIES",
    "EMPLOYMENT",
    "EXPORTS",
    "IMPORTS",
    "INVENTORIES",
    "ISM_MAN",
    "NEW_ORDERS",
    "ORDER_BACKLOG",
    "PRICES",
    "PRODUCTION"
]

# collection.delete_many({})

def insert_csv(doc, series):

    rows = []
    with open(doc, 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            rows.append(row)
    # print(header)
    # print(rows)
    data = []

    for r in rows:
        row = {}
        for i in range(len(header)):
            if header[i] == "date":
                values = r[i].split("/")
                date = datetime(int(values[-1]), int(values[0]), int(values[1])).strftime("%d/%m/%Y")
                row[header[i]] = date
            elif r[i] != '':
                row[header[i]] = float(r[i])
        data.append(row.copy())
    # print(json.dumps(data, indent=4))
    mongo_item = {
        'index': series,
        'data': data
    }
    collection.insert_one(mongo_item)

for i in range(len(filenames)):
    insert_csv(filenames[i], series_names[i])
