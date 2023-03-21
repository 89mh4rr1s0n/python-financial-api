from sqlalchemy import create_engine
import pandas as pd
import postgres_5
import requests
from datetime import datetime, date

db_string = 'postgresql://postgres:Fastman12@localhost:5432/python_test'
db = create_engine(db_string)

elements = ['HI', 'JO', 'LD', 'OS', 'QU', 'TS', 'UN', 'UO']

def insert_series(arr, provider, time):
  p = arr['period']
  d = arr['period_start_day']
  v = arr['value']
  df = pd.DataFrame(zip(p, d, v))
  df.columns = ['period', 'date', 'value']
  df['frequency'] = arr['@frequency']
  df['dataset_code'] = arr['dataset_code']
  df['dataset_name'] = arr['dataset_name']
  df['series_code'] = arr['series_code']
  df['series_name'] = arr['series_name']
  df['provider_code'] = provider['code']
  df['provider_name'] = provider['name']
  df['provider_region'] = provider['region']
  df['provider_website'] = provider['website']
  df['updated_at'] = time
  df['id'] = df['series_code'] + df['date']
  cols_at_end = ['id', 'dataset_name', 'series_name']
  df = df[[c for c in cols_at_end if c in df] +
          [c for c in df if c not in cols_at_end]]
  # print(df)
  postgres_5.upsert_df(df=df, table_name=postgres_5.to_snake(f"macro_{provider['slug']}_{arr['dataset_code']}"), engine=db)

def insert_key_stats(element):
    try:
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        data = requests.get(f'https://api.db.nomics.world/v22/series/BLS/jt?dimensions=%7B%22dataelement%22%3A%5B%22{element}%22%5D%7D&observations=1')
        data_json = data.json()

        for i in range(len(data_json['series']['docs'])):
          insert_series(data_json['series']['docs'][i], data_json['provider'], dt_string)

    except:
        pass


for element in elements:
    insert_key_stats(element)
    print(element)
