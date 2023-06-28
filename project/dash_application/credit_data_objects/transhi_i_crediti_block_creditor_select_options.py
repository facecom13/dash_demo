import dash_application.functions.convert_ral_excel_to_datafile as convert_ral_excel_to_datafile
import os
from sqlalchemy import create_engine
import pandas as pd

def transhi_i_crediti_block_creditor_select_options_func(data_input):
    df = pd.DataFrame()
    if data_input == '1с_api':
        url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
        engine = create_engine(url_db, pool_recycle=3600)

        with engine.connect() as con:
            query = 'SELECT creditor FROM "creditdb_2" GROUP BY creditor;'
            df = pd.read_sql(query, con)






    else:
        df = convert_ral_excel_to_datafile.get_credit_type_df()

    creditor_list = list(df['creditor'].unique())

    options_dict = {}
    for creditor in creditor_list:
        options_dict[creditor] = creditor
    options = options_dict

    return options
