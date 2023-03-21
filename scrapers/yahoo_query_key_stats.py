from sqlalchemy import create_engine
import pandas as pd
import postgres_5
from datetime import datetime, date
from yahooquery import Ticker

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


def insert_key_stats(ticker):
    try:
        item = Ticker(ticker)
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        df = pd.DataFrame(item.key_stats[ticker], index=[0])
        df['symbol'] = ticker
        df = df.rename(columns=postgres_5.to_snake)
        df['updated_at'] = dt_string
        df['id'] = df.apply(lambda row: postgres_5.does_exist(row, df.columns), axis=1)
        cols_at_end = ['id', 'symbol']
        df = df[[c for c in cols_at_end if c in df] +
                [c for c in df if c not in cols_at_end]]
        # print(df)
        postgres_5.upsert_df(df=df, table_name='key_stats', engine=db)
    except:
        pass


for symbol in symbols[:10]:
    insert_key_stats(symbol)
    print(symbol)
