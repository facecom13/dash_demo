import dash_application.functions.convert_ral_excel_to_datafile as convert_ral_excel_to_datafile
import os
from sqlalchemy import create_engine
import pandas as pd

def credit_line_type_select_options_func(data_input):
    df = pd.DataFrame()
    if data_input == '1с_api':
        url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
        engine = create_engine(url_db, pool_recycle=3600)

        with engine.connect() as con:
            query = 'SELECT credit_line_type FROM "creditdb_2" GROUP BY credit_line_type;'
            df = pd.read_sql(query, con)
    else:
        df = convert_ral_excel_to_datafile.get_credit_type_df()

    credit_line_type_list = list(df['credit_line_type'].unique())

    options_dict = {}
    for credit_line_type in credit_line_type_list:
        if credit_line_type == 'Возобновляемая' or credit_line_type == "Не возобновляемая":
            options_dict[credit_line_type] = credit_line_type
    options = options_dict

    return options
