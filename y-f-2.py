import yfinance as yf
import json

msft = yf.Ticker("CRNC")

# print(msft.calendar)
# print(msft.recommendations)
# print(msft.analysis)
# print(json.loads(msft.analysis.to_json(orient='records', date_format='iso', indent=4)))

response = json.loads(msft.recommendations.to_json(orient='records', date_format='iso', indent=4))

print(response)
# for i in response:
#     print(i)