from email import header
from flask import Flask, request, jsonify, make_response
from flask_restful import Api, Resource
from ib_insync import *
import random
import json
from bson import json_util
import yfinance as yf
import investpy
import datetime
import requests
from flask_apscheduler import APScheduler
# from scrapers import export_test.my_task
from scrapers.export_test import my_task

import pymongo
mongo_uri = "mongodb://localhost:27017"
client = pymongo.MongoClient(mongo_uri) 
db = client["financialModellingPrepDB"]
ism_man_coll = db["ismManufacturing"]
ism_serv_coll = db["ismServices"]
man_hist_collection = db["ismManHist"]
serv_hist_collection = db["ismServHist"]
itpm_collection = db["itpmData2"]

# nasdaq data link api key wXAfUqT2VxhmQzjMhsKW

random_id = random.randint(0, 9999)

ib = IB()
# ib.connect('127.0.0.1', 7496, clientId=1)

# ib.connect('127.0.0.1',
#             7496,
#             clientId=random_id,
#             timeout=0)

scheduler = APScheduler()
app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {"data": util.tree(ib.positions())}

# gspc = yf.Ticker("^GSPC")
# hist = gspc.history(period="max")

class Historical(Resource):
    def get(self, symbol):
        args = request.args
        gspc = yf.Ticker(symbol)
        period = "max"
        interval = "1d"

        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        if "interval" in args:
            interval = args.get("interval")

        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        if "period" in args:
            period = args.get("period")
        hist = gspc.history(period=period, interval=interval)
        return {
            "symbol": symbol,
            "data": json.loads(hist.reset_index().to_json(orient='records', date_format='iso'))
        }

class BondList(Resource):
    def get(self):
        return {
            "data": investpy.get_bonds_list()
        }

class BondHistorical(Resource):
    def get(self, country, duration):
        # bond_info = investpy.get_bond_information(bond=country + ' ' + duration)
        historical = investpy.get_bond_historical_data(bond=country + ' ' + duration, from_date='01/01/1950', to_date=datetime.datetime.today().strftime("%d/%m/%Y"))
        return {
            # "bond": json.loads(bond_info.to_json(orient='records')),
            "name": country + ' ' + duration,
            "historical": json.loads(historical.reset_index().to_json(orient='records', date_format='iso'))
        }

class CommodityList(Resource):
    def get(self):
        return investpy.get_commodities_list()

class CommidityHistorical(Resource):
    def get(self, commodity):
        historical = investpy.get_commodity_historical_data(commodity=commodity, from_date='01/01/1950', to_date=datetime.datetime.today().strftime("%d/%m/%Y"))
        return {
            "name": commodity,
            "historical": json.loads(historical.reset_index().to_json(orient='records', date_format='iso'))
        }
    
class MyCommodities(Resource):
    def get(self, commodity):
        if commodity == "copper-london":
            copper_lme = investpy.search.search_quotes(text='copper', products=["commodities"], countries=['united kingdom'])
            copper_lme_hist = copper_lme[0].retrieve_historical_data(from_date='01/01/1950', to_date=datetime.datetime.today().strftime("%d/%m/%Y"))
            return json.loads(copper_lme_hist.reset_index().to_json(orient='records', date_format='iso'))
        elif commodity == "copper-shanghai":
            copper_lme = investpy.search.search_quotes(text='copper', products=["commodities"], countries=['china'])
            copper_lme_hist = copper_lme[0].retrieve_historical_data(from_date='01/01/1950', to_date=datetime.datetime.today().strftime("%d/%m/%Y"))
            return json.loads(copper_lme_hist.reset_index().to_json(orient='records', date_format='iso'))
        elif commodity == "iron-chicago":
            copper_lme = investpy.search.search_quotes(text='iron-ore', products=["commodities"])
            copper_lme_hist = copper_lme[0].retrieve_historical_data(from_date='01/01/1950', to_date=datetime.datetime.today().strftime("%d/%m/%Y"))
            return json.loads(copper_lme_hist.reset_index().to_json(orient='records', date_format='iso'))
        elif commodity == "iron-shanghai":
            copper_lme = investpy.search.search_quotes(text='iron-ore', products=["commodities"], countries=["china"])
            copper_lme_hist = copper_lme[0].retrieve_historical_data(from_date='01/01/1950', to_date=datetime.datetime.today().strftime("%d/%m/%Y"))
            return json.loads(copper_lme_hist.reset_index().to_json(orient='records', date_format='iso'))

class ForexHistorical(Resource):
    def get(self, currency1, currency2):
        data = investpy.get_currency_cross_historical_data(currency_cross=currency1+"/"+currency2, from_date='01/01/1950', to_date=datetime.datetime.today().strftime("%d/%m/%Y"))
        return json.loads(data.reset_index().to_json(orient='records', date_format='iso'))

class IsmManufacturing(Resource):
    def get(self):
        mongo_response = ism_man_coll.find()
        items = [doc for doc in mongo_response]
        return jsonify(items)

class IsmServices(Resource):
    def get(self):
        mongo_response = ism_serv_coll.find()
        items = [doc for doc in mongo_response]
        return jsonify(items)

class IsmManHist(Resource):
    def get(self):
        mongo_response = man_hist_collection.find({},{ "_id": 0, "index": 1, "data": 1 })
        items = [doc for doc in mongo_response]
        return jsonify(items)

class IsmServHist(Resource):
    def get(self):
        mongo_response = serv_hist_collection.find({},{ "_id": 0, "index": 1, "data": 1 })
        items = [doc for doc in mongo_response]
        return jsonify(items)

class Itpm(Resource):
    def get(self):
        mongo_response = itpm_collection.find({},{ "_id": 0, "ratiosTTM": 0, })
        items = [doc for doc in mongo_response]
        return jsonify(items)


# cant be imported into excel -- throws extra characters at end of json input error
class ItpmRatiosTTM(Resource):
    def get(self):
        mongo_response = itpm_collection.find({},{"_id": 0, "symbol": 1, "ratiosTTM": 1,})
        items = [doc for doc in mongo_response]
        # return json.dumps(items)
        print(type(items))
        return {
            "data": items
        }
        # return jsonify(items)

class DbNomics(Resource):
    def get(self, provider, code):
        r = requests.get("https://api.db.nomics.world/v22/series/" + provider + "/" + code + "?dimensions=%7B%7D&observations=1")
        print(r)
        d = r.text
        djson = json.loads(d)
        datasets = djson["series"]["docs"]
        series = []
        for set in datasets:
            hist = []
            for x in range(len(set["period_start_day"])):
                item = {
                    'date': set["period_start_day"][x],
                    'value': set["value"][x]
                }
                hist.append(item.copy())
            s = {
                "name": set["series_name"],
                "historical": hist
            }
            series.append(s.copy())

        return {
            "name": djson["dataset"]["name"],
            "source": djson["provider"]["name"],
            "data": series
        }

class DbNomicsSingle(Resource):
    def get(self, provider, code, series):
        r = requests.get("https://api.db.nomics.world/v22/series/" + provider + "/" + code + "/" + series + "?observations=1")
        print(r)
        d = r.text
        djson = json.loads(d)
        datasets = djson["series"]["docs"]
        series = []
        for set in datasets:
            hist = []
            for x in range(len(set["period_start_day"])):
                item = {
                    'date': set["period_start_day"][x],
                    'value': set["value"][x]
                }
                hist.append(item.copy())
            s = {
                "name": set["series_name"],
                "historical": hist
            }
            series.append(s.copy())

        return {
            "name": djson["dataset"]["name"],
            "source": djson["provider"]["name"],
            "data": series
        }


# ib.positions()[0][1].symbol

# change following fundtion into a loop
def getOption(symbol, expiry, strike, right):
    contract = Option(
    # ib.portfolio()[1][0].symbol, 
    # ib.portfolio()[1][0].lastTradeDateOrContractMonth, 
    # ib.portfolio()[1][0].strike, 
    # ib.portfolio()[1][0].right,
    symbol,
    expiry,
    strike,
    right,
    'SMART'
    )
    details = ib.reqTickers(contract)

def job1():
    print('dsghtwe')

# api.add_resource(HelloWorld, "/helloworld")
api.add_resource(Historical, "/historical/<string:symbol>")
api.add_resource(BondList, "/available-bonds")
api.add_resource(BondHistorical, "/historical/bond/<string:country>/<string:duration>")
api.add_resource(CommodityList, "/available-commodities")
api.add_resource(CommidityHistorical, "/historical/commodity/<string:commodity>")
api.add_resource(MyCommodities, "/my-commodity/<string:commodity>")
api.add_resource(ForexHistorical, "/forex/historical/<string:currency1>-<string:currency2>")
api.add_resource(DbNomics, "/dbn/<string:provider>/<string:code>")
api.add_resource(DbNomicsSingle, "/dbn-single/<string:provider>/<string:code>/<string:series>")
api.add_resource(IsmManufacturing, "/ism-man")
api.add_resource(IsmServices, "/ism-non-man")
api.add_resource(IsmManHist, "/ism-man-hist")
api.add_resource(IsmServHist, "/ism-serv-hist")
api.add_resource(Itpm, "/itpm")
api.add_resource(ItpmRatiosTTM, "/itpm-ratios")

@scheduler.task('interval', id='my_job', seconds = 4)
def my_job():
    my_task()

if __name__ == "__main__":
    # scheduler.add_job(id='mytask', func=export_test.my_task(), trigger = 'interval', seconds = 4)
    scheduler.start()
    app.run(debug=True, use_reloader=False)