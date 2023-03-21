from sqlalchemy import create_engine
import pandas as pd
import requests
import scrapers.postgres_5 as postgres_5
from datetime import datetime, date

db_string = 'postgresql://postgres:Fastman12@localhost:5432/python_test'
db = create_engine(db_string)

query = db.execute("""  
select * from profiles
where exchange_short_name = 'NASDAQ' 
and is_fund = 'false'
and mkt_cap > 1
order by mkt_cap desc  
""")

symbols = []

for r in query:
    symbols.append(r['symbol'])

start_date = date(1950, 1, 1)  # yr-mth-day
end_date = date.today()    # perhaps date.now()

# print(symbols[:10])

dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
data = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/{symbols[0]}?apikey=e812649ac124bbb4d773e2ff24a28f0d')
data_json = data.json()
df = pd.DataFrame(data_json['historical'])
df['symbol'] = data_json['symbol']
# df = pd.DataFrame.from_dict(data_json)
df = df.rename(columns=postgres_5.to_snake)
df['id'] = df.apply(
        lambda row: postgres_5.does_exist(row, df.columns), axis=1)
df['updated_at'] = dt_string
df = df.drop(['change', 'change_percent', 'label', 'vwap', 'unadjusted_volume', 'change_over_time'], axis=1)
cols_at_end = ['id', 'symbol']
df = df[[c for c in cols_at_end if c in df] +
        [c for c in df if c not in cols_at_end]]
postgres_5.upsert_df(df=df, table_name='historical_prices_daily', engine=db)
print(df)