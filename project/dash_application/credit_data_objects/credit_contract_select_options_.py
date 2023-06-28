import dash_application.functions.convert_ral_excel_to_datafile as convert_ral_excel_to_datafile
import os
from sqlalchemy import create_engine
import pandas as pd

def credit_contract_select_options_func(data_input, creditor_select):
    df = pd.DataFrame()
    if data_input == '1с_api':
        url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
        engine = create_engine(url_db, pool_recycle=3600)

        with engine.connect() as con:
            query = 'SELECT credit_contract, creditor FROM "creditdb_2" GROUP BY credit_contract, creditor;'
            df = pd.read_sql(query, con)
    else:
        df = convert_ral_excel_to_datafile.get_credit_type_df()


    creditor_full_list = list(df['creditor'].unique())
    creditor_filter = creditor_full_list
    if creditor_select:
        if 'list' in str(type(creditor_select)):
            creditor_filter = creditor_select
        else:
            creditor_filter = list(creditor_select)
    # режем выборку по кредитору
    df = df.loc[df['creditor'].isin(creditor_filter)]



    credit_contract_list = list(df['credit_contract'].unique())

    options_dict = {}
    for credit_contract in credit_contract_list:
        options_dict[credit_contract] = credit_contract
    options = options_dict

    return options
