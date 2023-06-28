import psycopg2

import os
from sqlalchemy import create_engine
import pandas as pd
def leasing_rate_distribution_barchart_year_select_options_func(data_input, leasing_table):
    if data_input == '1с_api':
        url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
        engine = create_engine(url_db, pool_recycle=3600)

        with engine.connect() as con:
            query = f'SELECT year FROM {leasing_table} GROUP BY year;'
            df = pd.read_sql(query, con)

        year_list = list(df['year'].unique())

        options_dict = {}
        for year in year_list:
            year = int(year)
            options_dict[year] = year
        options = options_dict

        return options