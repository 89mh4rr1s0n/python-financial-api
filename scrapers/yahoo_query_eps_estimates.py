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


def insert_earnings_trend(ticker):
    try:
        item = Ticker(ticker)
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        df = pd.DataFrame(item.earnings_trend[ticker]['trend'])
        df = pd.concat([
            df.drop(['earningsEstimate', 'revenueEstimate',
                    'epsTrend', 'epsRevisions', 'growth', 'maxAge'], axis=1),
            df['earningsEstimate'].apply(pd.Series).add_prefix('eps_est_'),
            df['revenueEstimate'].apply(pd.Series).add_prefix('rev_est_'),
            df['epsTrend'].apply(pd.Series).add_prefix('eps_trend_'),
            df['epsRevisions'].apply(pd.Series).add_prefix('eps_revisions_')
        ], axis=1)
        df.drop(df.tail(2).index,
                inplace=True)
        df['symbol'] = ticker
        df = df.rename(columns=postgres_5.to_snake)
        df['id'] = df.apply(
            lambda row: postgres_5.does_exist(row, df.columns), axis=1)
        df['updated_at'] = dt_string
        df = df.rename(columns={'period': 'time'})
        df['period'] = df.loc[:, 'time']
        df = (df
              .replace({'period': {'0q': 'current_quarter'}})
              .replace({'period': {'+1q': 'next_quarter'}})
              .replace({'period': {'0y': 'current_year'}})
              .replace({'period': {'+1y': 'next_year'}}))
        df = df.drop(['eps_revisions_down_last90days'], axis=1)
        cols_at_end = ['id', 'symbol']
        df = df[[c for c in cols_at_end if c in df] +
                [c for c in df if c not in cols_at_end]]
        # print(df)
        postgres_5.upsert_df(df=df, table_name='analyst_estimates', engine=db)
    except:
        print('dh')


for symbol in symbols[:1]:
    insert_earnings_trend(symbol)
    print(symbol)
