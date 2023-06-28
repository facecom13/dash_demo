import dash_application.functions.convert_ral_excel_to_datafile as convert_ral_excel_to_datafile
import os
from sqlalchemy import create_engine
import pandas as pd
import dash_application.functions.mapping as mapping

def credit_tab_month_select_options_func(data_input):
    df = pd.DataFrame()
    if data_input == '1с_api':
        url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
        engine = create_engine(url_db, pool_recycle=3600)

        with engine.connect() as con:
            query = 'SELECT date FROM "creditdb_2" GROUP BY date;'
            df = pd.read_sql(query, con)
    else:
        df = convert_ral_excel_to_datafile.get_credit_type_df()

    df['date_2'] = pd.to_datetime(df['date'])
    if "int" in str(df['date'].dtype):
        df['date_2'] = pd.to_datetime(df['date'], unit='ms')
    df['month'] = df['date_2'].dt.month

    list_for_credit_tab_month_select_options = list(df['month'])
    unique_list = set(list_for_credit_tab_month_select_options)
    options_dict = {}
    month_mapping_dict = mapping.month_mapping()
    # print(month_mapping_dict)
    for item in unique_list:
        options_dict[item] = month_mapping_dict[item]

    return options_dict