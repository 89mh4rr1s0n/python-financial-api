from flask import Flask, request
from flask_restful import Api, Resource
from ib_insync import *
import random
import json
import yfinance as yf
import investpy
import datetime
import requests

# nasdaq data link api key wXAfUqT2VxhmQzjMhsKW

random_id = random.randint(0, 9999)

ib = IB()
# ib.connect('127.0.0.1', 7496, clientId=1)

# ib.connect('127.0.0.1',
#             7496,
#             clientId=random_id,
#             timeout=0)

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

# api.add_resource(HelloWorld, "/helloworld")
api.add_resource(Historical, "/historical/<string:symbol>")
api.add_resource(BondList, "/available-bonds")
api.add_resource(BondHistorical, "/historical/bond/<string:country>/<string:duration>")
api.add_resource(DbNomics, "/dbn/<string:provider>/<string:code>")
api.add_resource(DbNomicsSingle, "/dbn-single/<string:provider>/<string:code>/<string:series>")

if __name__ == "__main__":
    app.run(debug=True)