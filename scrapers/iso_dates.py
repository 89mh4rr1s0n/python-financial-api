from datetime import date, timedelta
import scrapers.postgres_5 as postgres_5

start_date = date(2008, 8, 15)  # yr-mth-day
end_date = date.today()    # perhaps date.now()
delta = end_date - start_date   # returns timedelta
dates = []

for i in range(delta.days + 1):
    day = start_date + timedelta(days=i)
    dates.append(day)

print(dates[-6:-1])

'https://financialmodelingprep.com/api/v4/batch-request-end-of-day-prices?date=2021-05-18&apikey=e812649ac124bbb4d773e2ff24a28f0d'

for i in range(5):
  postgres_5.insert_data(
    f'https://financialmodelingprep.com/api/v4/batch-request-end-of-day-prices?date={dates[i-5]}&apikey=e812649ac124bbb4d773e2ff24a28f0d',
    'historical_prices_daily',
    f'Historical Prices Daily - {dates[i-5]}'
  )