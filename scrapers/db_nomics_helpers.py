import pandas as pd
import postgres_5 as pg5
from sqlalchemy import create_engine

db_string = 'postgresql://postgres:Fastman12@localhost:5432/python_test'
db = create_engine(db_string)

def insert_db_nomics_series(arr, provider, time):
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
  if provider['code'] == 'OECD' and arr['dataset_code'] == "REV":
    df['provider_region'] = arr['dimensions']['COU']
  elif provider['code'] == 'OECD' and arr['dataset_code'] == "ALFS_EMP" or provider['code'] == 'OECD' and arr['dataset_code'] == "QNA":
    df['provider_region'] = arr['dimensions']['LOCATION']
  else:
    df['provider_region'] = provider['region']

  df['provider_website'] = provider['website']
  df['updated_at'] = time
  df['value'] = pd.to_numeric(df['value'], errors='coerce')
  df['id'] = df['series_code'] + df['date']
  cols_at_end = ['id', 'dataset_name', 'series_name']
  df = df[[c for c in cols_at_end if c in df] +
          [c for c in df if c not in cols_at_end]]
  # print(df)
  pg5.upsert_df(df=df, table_name=pg5.to_snake(f"macro_{provider['slug']}_{arr['dataset_code']}"), engine=db)