# Upsert function for pandas to_sql with postgres
# https://stackoverflow.com/questions/1109061/insert-on-duplicate-update-in-postgresql/8702291#8702291
# https://www.postgresql.org/docs/devel/sql-insert.html#SQL-ON-CONFLICT
import pandas as pd
import sqlalchemy
import uuid
import re
from datetime import datetime
import dask.dataframe as dd

def to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def does_exist(row, arr):
    s = row['symbol'] if 'symbol' in arr else ''
    d = row['date'] if 'date' in arr else ''
    p = row['period'] if 'period' in arr else ''
    return f'{s}{d}{p}'


def upsert_df(df: pd.DataFrame, table_name: str, engine: sqlalchemy.engine.Engine):
    """Implements the equivalent of pd.DataFrame.to_sql(..., if_exists='update')
    (which does not exist). Creates or updates the db records based on the
    dataframe records.
    Conflicts to determine update are based on the dataframes index.
    This will set primary keys on the table equal to the index names

    1. Create a temp table from the dataframe
    2. Insert/update from temp table into table_name

    Returns: True if successful

    """

    engine = sqlalchemy.create_engine(
          'postgresql://postgres:Fastman12@localhost:5432/python_test')

    # If the table does not exist, we should just use to_sql to create it
    if not engine.execute(
        f"""SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE  table_schema = 'public'
            AND    table_name   = '{table_name}');
            """
    ).first()[0]:
        df.to_sql(table_name, uri=engine)
        return True

    # If it already exists...
    temp_table_name = f"temp_{uuid.uuid4().hex[:6]}"
    df.to_sql(temp_table_name, uri=engine, index=True)

    index = list(df.index.names)
    index_sql_txt = ", ".join([f'"{i}"' for i in index])
    columns = list(df.columns)
    headers = columns
    headers_sql_txt = ", ".join(
        [f'"{i}"' for i in headers]
    )  # index1, index2, ..., column 1, col2, ...

    # col1 = exluded.col1, col2=excluded.col2
    update_column_stmt = ", ".join(
        [f'"{col}" = EXCLUDED."{col}"' for col in columns])

    # For the ON CONFLICT clause, postgres requires that the columns have unique constraint
    query_pk = f"""
    ALTER TABLE "{table_name}" ADD CONSTRAINT {table_name}_unique_constraint_for_upsert UNIQUE (id);
    """
    try:
        engine.execute(query_pk)
    except Exception as e:
        # relation "unique_constraint_for_upsert" already exists
        if not 'unique_constraint_for_upsert" already exists' in e.args[0]:
            raise e

    # Compose and execute upsert query
    query_upsert = f"""
    INSERT INTO "{table_name}" ({headers_sql_txt}) 
    SELECT {headers_sql_txt} FROM "{temp_table_name}"
    ON CONFLICT (id) DO UPDATE 
    SET {update_column_stmt};
    """
    engine.execute(query_upsert)
    engine.execute(f'DROP TABLE "{temp_table_name}"')

    return True

def insert_data(url, t_name, title):
  if __name__ == "__main__":
      # TESTS (create environment variable DB_STR to do it)
      dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
      engine = sqlalchemy.create_engine(
          'postgresql://postgres:Fastman12@localhost:5432/python_test')
      indexes = ["id"]
      # dataframe
      df = dd.read_csv(url, dtype={'calendarYear': 'float64'})
      df = df.rename(columns=to_snake)
      df['id'] = df.apply(lambda row: does_exist(row, df.columns), meta=(None, 'object'), axis=1)
      df['updated_at'] = dt_string
      # df.set_index('id')
      cols_at_end = ['id']
      df = df[[c for c in cols_at_end if c in df] +
              [c for c in df if c not in cols_at_end]]

      print(df.head(5))
      # TNAME = "test_upsert_df"
      # upsert_df(df=df, table_name=t_name, engine=engine) # for pandas
      upsert_df(df=df, table_name=t_name, engine='postgresql://postgres:Fastman12@localhost:5432/python_test')
      print(datetime.now().strftime("%d/%m/%Y %H:%M:%S" + ' finished inserting ' + title))

print(datetime.now().strftime("%d/%m/%Y %H:%M:%S" + ' started inserting '))
insert_data(
  "https://financialmodelingprep.com/api/v4/income-statement-bulk?year=2021&period=quarter&apikey=e812649ac124bbb4d773e2ff24a28f0d",
  "test_dask",
  "first test"
  )
