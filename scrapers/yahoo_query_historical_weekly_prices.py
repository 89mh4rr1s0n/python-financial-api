import numpy as np
from sqlalchemy import create_engine
import pandas as pd
import postgres_5 as postgres_5
from datetime import datetime, date
from yahooquery import Ticker

db_string = 'postgresql://postgres:Fastman12@localhost:5432/python_test'
db = create_engine(db_string)

query = db.execute("""
select * from profiles
where exchange_short_name = 'NASDAQ'
and symbol != 'FB'
and is_fund = 'false'
and mkt_cap > 1
order by mkt_cap desc
""")

symbols = []

def chunk_array(array, chunk_size):
    return [array[i:i + chunk_size] for i in range(0, len(array), chunk_size)]

for r in query:
    symbols.append(r['symbol'])

chunks = chunk_array(symbols, 5)

def insert_earnings_trend(tickers):
    try:
        items = Ticker(tickers, asynchronous=True)
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        df = pd.DataFrame(items.history(period='1y', interval='1wk')).reset_index()
        df = df.rename(columns=postgres_5.to_snake)
        df = df[['symbol', 'date', 'open', 'high', 'low', 'close', 'adjclose', 'volume']]
        df['id'] = df.apply(lambda row: postgres_5.does_exist(row, df.columns), axis=1)
        df['updated_at'] = dt_string
        cols_at_end = ['id', 'symbol']
        df = df[[c for c in cols_at_end if c in df] +
                [c for c in df if c not in cols_at_end]]
        df['my_dates'] = pd.to_datetime(df['date'])
        df['day_of_week'] = df['my_dates'].dt.day_name()
        df = df[df['open'].notnull()]
        df['diff'] = df.groupby('symbol')['date'].diff() / np.timedelta64(1, 'D')
        df['diff'] = df['diff'].fillna(7)
        df = df.query("`diff` > 5")
        # print(df)
        postgres_5.upsert_df(df=df, table_name='historical_prices_weekly', engine=db)
    except:
        try:
            for ticker in tickers:
              try:
                i = Ticker(ticker)
                dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                df = pd.DataFrame(i.history(period='1y', interval='1wk')).reset_index()
                df = df.rename(columns=postgres_5.to_snake)
                df = df[['symbol', 'date', 'open', 'high', 'low', 'close', 'adjclose', 'volume']]
                df.rename(columns={'adjclose': 'adj_close'})
                df['id'] = df.apply(lambda row: postgres_5.does_exist(row, df.columns), axis=1)
                df['updated_at'] = dt_string
                cols_at_end = ['id', 'symbol']
                df = df[[c for c in cols_at_end if c in df] +
                        [c for c in df if c not in cols_at_end]]
                df['my_dates'] = pd.to_datetime(df['date'])
                df['day_of_week'] = df['my_dates'].dt.day_name()
                df = df[df['open'].notnull()]
                df['diff'] = df.groupby('symbol')['date'].diff() / np.timedelta64(1, 'D')
                df['diff'] = df['diff'].fillna(7)
                df = df.query("`diff` > 5")
                # print(df)
                print(ticker)
                postgres_5.upsert_df(df=df, table_name='historical_prices_weekly', engine=db)
              except:
                # print(f'{ticker} error1')
                pass
        except:
              # print(f'{ticker} error2')
              pass

for chunk in chunks[:15]:
    insert_earnings_trend(chunk)
    print(chunk)
