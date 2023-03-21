import pandas as pd
import psycopg2
import requests
import re
from datetime import datetime
from sqlalchemy import create_engine

def to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

def does_exist(row, arr):
  s = row['symbol'] if 'symbol' in arr else ''
  d = row['date'] if 'date' in arr else ''
  p = row['period'] if 'period' in arr else ''
  return f'{s}{d}{p}'

def col_type(str):
  if str == 'id':
    return 'TEXT PRIMARY KEY'
  if str == 'object':
    return 'TEXT'
  elif str == 'bool':
    return 'BOOLEAN'
  else: return 'FLOAT'
  # if '64' in str:
  #   return 'FLOAT'

dtypes = {
  'Symbol':                'string',
  'Price':                'float64',
  'Beta':                 'float64',
  'VolAvg':                 'int64',
  'MktCap':               'float64',
  'LastDiv':              'float64',
  'Range':                 'string',
  'Changes':              'float64',
  'companyName':           'string',
  'currency':              'string',
  'cik':                  'float64',
  'isin':                  'string',
  'cusip':                 'string',
  'exchange':              'string',
  'exchangeShortName':     'string',
  'industry':              'string',
  'website':               'string',
  'description':           'string',
  'CEO':                   'string',
  'sector':                'string',
  'country':               'string',
  'fullTimeEmployees':     'string',
  'phone':                 'string',
  'address':               'string',
  'city':                  'string',
  'state':                 'string',
  'zip':                   'string',
  'DCF_diff':             'float64',
  'DCF':                  'float64',
  'image':                 'string',
  'ipoDate':               'string',
  'defaultImage':            'bool',
  'isEtf':                   'bool',
  'isActivelyTrading':       'bool',
  'isFund':                  'bool',
  'isAdr':                   'bool',
}

def insert_data(url, table_name):
  conn = psycopg2.connect("dbname=python_test user=postgres password=Fastman12")
  engine = create_engine('postgresql://postgres:Fastman12@localhost:5432/python_test')
  cursor = conn.cursor()
  now = datetime.now()
  dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

# fast 25 seconds for income statement qtrly 2022
  response = requests.get(url)
  if response.status_code == 200:
      df = pd.read_csv(url, engine='python')
      # print(df.dtypes.to_dict())
      df = df.rename(columns=to_snake)
      df['id'] = df.apply(lambda row: does_exist(row, df.columns), axis=1)
      df['updated_at'] = dt_string
      df.set_index('id')
      cols_at_end = ['id']
      df = df[
        [c for c in cols_at_end if c in df]
        + 
        [c for c in df if c not in cols_at_end] 
        ]
      conn.commit()
      df.to_sql(table_name, engine, if_exists='replace', index=False)
      print(datetime.now().strftime("%d/%m/%Y %H:%M:%S" + ' finished insert'))
  else:
      print("Failed to retrieve data")

print(datetime.now().strftime("%d/%m/%Y %H:%M:%S" + ' starting insert'))
insert_data("https://financialmodelingprep.com/api/v4/income-statement-bulk?year=2022&period=quarter&apikey=e812649ac124bbb4d773e2ff24a28f0d", 'income_statement_qtrly')