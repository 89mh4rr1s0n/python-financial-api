import sqlalchemy
db_string = 'postgresql://postgres:Fastman12@localhost:5432/python_test'
db = sqlalchemy.create_engine(db_string)
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(db)

qry = text("""
DO $$
DECLARE
    table_record record;
BEGIN
    FOR table_record IN (SELECT tablename FROM pg_tables WHERE tablename like 'temp_%') LOOP
        EXECUTE 'DROP TABLE IF EXISTS ' || table_record.tablename || ' CASCADE';
    END LOOP;
END $$;
""")

def execute():
    with Session() as connection:
        connection.execute(qry)
        connection.commit()


  

