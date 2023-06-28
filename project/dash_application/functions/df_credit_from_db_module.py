import psycopg2
import os
import pandas as pd

from sqlalchemy import create_engine
def df_credit_from_db_func():
    url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
    engine = create_engine(url_db, pool_recycle=3600)
    df = pd.read_sql_query('select * from "creditDB"', con=engine)
    try:
        df['date'] = pd.to_datetime(df['date'])
    except:
        pass

    try:
        df['credit_tranch_date'] = pd.to_datetime(df['credit_tranch_date'])
    except:
        pass

    try:
        df['month_first_date'] = pd.to_datetime(df['credit_tranch_date'])
    except:
        pass

    return df