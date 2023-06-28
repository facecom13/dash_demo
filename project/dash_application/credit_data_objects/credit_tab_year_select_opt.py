import datetime

import dash_application.functions.convert_ral_excel_to_datafile as convert_ral_excel_to_datafile
import os
from sqlalchemy import create_engine
import pandas as pd

def credit_tab_year_select_options_func(data_input):
    df = pd.DataFrame()
    if data_input == '1с_api':
        url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
        engine = create_engine(url_db, pool_recycle=3600)

        with engine.connect() as con:
            query = 'SELECT year FROM "creditdb_2" GROUP BY year;'
            df = pd.read_sql(query, con)
    else:
        df = convert_ral_excel_to_datafile.get_credit_type_df()

    year_list = list(df['year'].unique())


    options_dict = {}
    for year in year_list:
        if int(year)>=datetime.datetime.now().year:
            options_dict[int(year)] = int(year)
    options = options_dict

    return options
