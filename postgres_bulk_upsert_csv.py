import pandas as pd
import psycopg2
import requests
import re
from datetime import datetime
import sqlalchemy as db
import uuid

def to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

def does_exist(row, arr):
  s = row['symbol'] if 'symbol' in arr else ''
  d = row['date'] if 'date' in arr else ''
  p = row['period'] if 'period' in arr else ''
  return f'{s}{d}{p}'

def col_type(str):
  if str == 'object':
    return 'TEXT'
  elif str == 'bool':
    return 'BOOLEAN'
  else: return 'FLOAT'

def create_upsert_method(meta: db.MetaData):
    """
    Create upsert method that satisfied the pandas's to_sql API.
    """
    def method(table, conn, keys, data_iter):
        # select table that data is being inserted to (from pandas's context)
        sql_table = db.Table(table.name, meta, autoload=True)
        
        # list of dictionaries {col_name: value} of data to insert
        values_to_insert = [dict(zip(keys, data)) for data in data_iter]
        
        # create insert statement using postgresql dialect.
        # For other dialects, please refer to https://docs.sqlalchemy.org/en/14/dialects/
        insert_stmt = db.dialects.postgresql.insert(sql_table, values_to_insert)

        # create update statement for excluded fields on conflict
        update_stmt = {exc_k.key: exc_k for exc_k in insert_stmt.excluded}
        
        # create upsert statement. 
        upsert_stmt = insert_stmt.on_conflict_do_update(
            index_elements=sql_table.primary_key.columns, # index elements are primary keys of a table
            set_=update_stmt # the SET part of an INSERT statement
        )
        
        # execute upsert statement
        conn.execute(upsert_stmt)

    return method

# create postgres db engine
# db_engine = db.create_engine(f"postgresql://{user}:{password}@{host}:5432/{database}")
db_engine = db.create_engine('postgresql://postgres:Fastman12@localhost:5432/python_test')

# create DB metadata object that can access table names, primary keys, etc.
meta = db.MetaData(db_engine)

# create upsert method that is accepted by pandas API
upsert_method = create_upsert_method(meta)

def insert_data(url, table_name):
  conn = psycopg2.connect("dbname=python_test user=postgres password=Fastman12")
  # engine = create_engine('postgresql://postgres:Fastman12@localhost:5432/python_test')
  cursor = conn.cursor()
  now = datetime.now()
  dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

  response = requests.get(url)
  if response.status_code == 200:
      df = pd.read_csv(url, engine='python')
      # print(df.dtypes.to_dict())
      df = df.rename(columns=to_snake)
      df['id'] = df.apply(lambda row: does_exist(row, df.columns), axis=1)
      df['updated_at'] = dt_string
      create_table_qry = f'CREATE TABLE IF NOT EXISTS {table_name} ('
      for i in range(len(df.dtypes)):
        column_type = col_type(df[df.columns[i]].dtype)
        create_table_qry += f' {df.columns[i]} {column_type},'
        
      create_table_qry = create_table_qry[:-1]
      create_table_qry += ')'
      create_table_qry = create_table_qry.replace('id TEXT', 'id TEXT PRIMARY KEY')
      cursor.execute(create_table_qry)
      # cursor.execute(f""" ALTER TABLE {table_name} ADD PRIMARY KEY(id) """)
      conn.commit()
      df.to_sql(
        table_name, 
        db_engine,
        schema=db.schema,
        if_exists='replace',
        index=False,
        method=upsert_method
        )
      print(datetime.now().strftime("%d/%m/%Y %H:%M:%S" + ' finished insert'))
  else:
      print("Failed to retrieve data")

print(datetime.now().strftime("%d/%m/%Y %H:%M:%S" + ' starting insert'))
insert_data("https://financialmodelingprep.com/api/v4/income-statement-bulk?year=2022&period=quarter&apikey=e812649ac124bbb4d773e2ff24a28f0d", 'income_statement_qtrly')