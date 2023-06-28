import os
from sqlalchemy import create_engine
import pandas as pd


def revenue_range_select_options_func():
    url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
    engine = create_engine(url_db, pool_recycle=3600)
    with engine.connect() as con:
        query = 'SELECT *  FROM "revenue_ranges";'
        df = pd.read_sql(query, con)

    list_of_revenue_ranges = list(df['range_name'])

    revenue_range_select_options = {}
    for item in list_of_revenue_ranges:
        revenue_range_select_options[item] = item

    return revenue_range_select_options