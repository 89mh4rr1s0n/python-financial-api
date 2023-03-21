from sqlalchemy import create_engine
import pandas as pd
import requests
import scrapers.postgres_5 as postgres_5
from datetime import datetime

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

# rate limit with delay needed?

def chunk_array(array, chunk_size):
    return [array[i:i + chunk_size] for i in range(0, len(array), chunk_size)]


def getData(url, t_name, title):
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    d = requests.get(url)
    dj = d.json()
    df = pd.DataFrame(dj)
    df = df.rename(columns=postgres_5.to_snake)
    df['id'] = df.apply(
        lambda row: postgres_5.does_exist(row, df.columns), axis=1)
    df['updated_at'] = dt_string
    df.set_index('id')
    cols_at_end = ['id']
    df = df[[c for c in cols_at_end if c in df] +
            [c for c in df if c not in cols_at_end]]
    # print(df)
    postgres_5.upsert_df(df=df, table_name=t_name, engine=db)
    print('inserted price changes')

for r in query:
    symbols.append(r['symbol'])

chunks = chunk_array(symbols, 300)

for chunk in chunks:
    param = ','.join(str(number) for number in chunk)
    getData(
        f'https://financialmodelingprep.com/api/v3/stock-price-change/{param}?apikey=e812649ac124bbb4d773e2ff24a28f0d',
        'price_changes',
        'Price Changes'
    )
