from ib_insync import *
import json
# util.startLoop()  # uncomment this line when in a notebook

ib = IB()
ib.connect('127.0.0.1', 7496, clientId=1)

# retrieve data for ATKR stock
atkr = Stock('ATKR', 'SMART', 'USD')

# retrieve data for EURUSD forex pair
contract = Forex('EURUSD')


bars = ib.reqHistoricalData(
    atkr, endDateTime='', durationStr='30 D',
    barSizeSetting='1 hour', whatToShow='MIDPOINT', useRTH=True)

# convert to pandas dataframe:
# df = util.df(bars)
# print(df)

# print(type(ib.positions()[0][1]))
# print(ib.positions()[0])
# print(ib.positions()[0][1].symbol)

print(ib.portfolio()[1][0].strike)
# print(ib.accountSummary())

def onPendingTicker(ticker):
    print("pending ticker received")
    print(ticker)

contract = Option(
    ib.portfolio()[0][0].symbol, 
    ib.portfolio()[0][0].lastTradeDateOrContractMonth, 
    ib.portfolio()[0][0].strike, 
    ib.portfolio()[0][0].right,
    'SMART'
    )

stock = Stock('AMD', 'SMART', 'USD')

# details = ib.reqTickers(contract)
details = ib.reqMktData(contract)
print (details)
ib.pendingTickersEvent += onPendingTicker

positions = util.tree(ib.positions())
print(len(positions))

# for p in positions:
#     if "Option" in p["contract"]:
#         print('This is an Option position')
#         print(p)
#         contract = Option(
#             p["contract"]["Option"]["symbol"], 
#             p["contract"]["Option"]["lastTradeDateOrContractMonth"], 
#             p["contract"]["Option"]["strike"], 
#             p["contract"]["Option"]["right"],
#             'SMART'
#             )
#         details = ib.reqTickers(contract)
#         print(details)
#         # ib.pendingTickersEvent += onPendingTicker
#     else:
#         print("This is NOT an option position")
#         print(p)
    

# print(ib.positions()[0].position)





ib.run()