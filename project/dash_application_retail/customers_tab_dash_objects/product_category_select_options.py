import dash_application.functions.convert_ral_excel_to_datafile as convert_ral_excel_to_datafile
import os
from sqlalchemy import create_engine
import pandas as pd
import dash_application.functions.mapping as mapping

def product_category_select_options_func():
    url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
    engine = create_engine(url_db, pool_recycle=3600)

    with engine.connect() as con:
        query = 'SELECT product_category FROM "customer_product_category" GROUP BY product_category;'
        df = pd.read_sql(query, con)

    df.sort_values(['product_category'], inplace=True)
    product_category_list = list(df['product_category'].unique())

    options_dict = {}
    for item in product_category_list:
        options_dict[item] = item

    return options_dict


