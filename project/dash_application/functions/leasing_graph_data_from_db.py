import psycopg2

import pandas as pd
import os
from sqlalchemy import create_engine
def leasing_graph_data_from_db_func():
    url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
    engine = create_engine(url_db, pool_recycle=3600)
    query = 'SELECT * FROM "leasingDB" ;'
    df = pd.read_sql_query(query, con=engine)
    return df