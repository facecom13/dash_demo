import datetime

import dash_application.functions.select_options as select_options
import pandas as pd
def credit_tab_year_select_options_func(df):
    # print(df.info())

    # df = df.loc[df['year']>=2023]
    df['date_2'] = pd.to_datetime(df['date'])
    df = df.loc[df['date_2'] >= datetime.datetime(2023, 1, 1)]

    if "int" in str(df['date'].dtype):
        df['date_2'] = pd.to_datetime(df['date'], unit='ms')
    df = df.copy()
    df['year'] = df['date_2'].dt.year
    df['quarter'] = df['date_2'].dt.quarter

    list_for_credit_tab_year_select_options = list(df['year'])
    credit_tab_year_select_options = select_options.select_options_func(list_for_credit_tab_year_select_options)

    return credit_tab_year_select_options