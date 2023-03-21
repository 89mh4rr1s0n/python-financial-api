# Upsert function for pandas to_sql with postgres
# https://stackoverflow.com/questions/1109061/insert-on-duplicate-update-in-postgresql/8702291#8702291
# https://www.postgresql.org/docs/devel/sql-insert.html#SQL-ON-CONFLICT
import pandas as pd
import sqlalchemy
import uuid
import requests
import re
from datetime import datetime

def to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

def does_exist(row, arr):
    s = row['symbol'] if 'symbol' in arr else ''
    d = row['date'] if 'date' in arr else ''
    p = row['period'] if 'period' in arr else ''
    return f'{s}{d}{p}'

def upsert_df(df: pd.DataFrame, table_name: str, engine: sqlalchemy.engine.Engine):
    if not engine.execute(
        f"""SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE  table_schema = 'public'
            AND    table_name   = '{table_name}');
            """
    ).first()[0]:
        df.to_sql(table_name, engine, index=True)
        return True

    # If it already exists...
    temp_table_name = f"temp_{uuid.uuid4().hex[:6]}"
    df.to_sql(temp_table_name, engine, index=True)

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
    engine.execute(f'DROP TABLE {temp_table_name}')

    return True

def insert_data(url, t_name, title):
  if __name__ == "__main__":
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    engine = sqlalchemy.create_engine(
        'postgresql://postgres:Fastman12@localhost:5432/python_test')
    indexes = ["id"]
    df = pd.read_csv(url, engine='python')
    df = df.rename(columns=to_snake)
    df['id'] = df.apply(lambda row: does_exist(row, df.columns), axis=1)
    df['updated_at'] = dt_string
    df.set_index('id')
    cols_at_end = ['id']
    df = df[[c for c in cols_at_end if c in df] +
            [c for c in df if c not in cols_at_end]]

    TNAME = "upsert_df"
    upsert_df(df=df, table_name=t_name, engine=engine)
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S" + ' finished inserting ' + title))

# print(datetime.now().strftime("%d/%m/%Y %H:%M:%S" + ' starting insert'))

# url = "https://financialmodelingprep.com/api/v4/income-statement-bulk?year=2023&period=quarter&apikey=e812649ac124bbb4d773e2ff24a28f0d"

print(datetime.now().strftime("%d/%m/%Y %H:%M:%S" + ' started inserting '))
insert_data(
  "https://financialmodelingprep.com/api/v4/income-statement-bulk?year=2022&period=quarter&apikey=e812649ac124bbb4d773e2ff24a28f0d",
  "upsert_df",
  "first test"
  )
