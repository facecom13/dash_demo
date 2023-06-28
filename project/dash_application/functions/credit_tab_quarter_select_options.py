import dash_application.functions.select_options as select_options
import pandas as pd
def credit_tab_quarter_select_options_func(df):
    df['date_2'] = pd.to_datetime(df['date'])
    if "int" in str(df['date'].dtype):
        df['date_2'] = pd.to_datetime(df['date'], unit='ms')
    df['year'] = df['date_2'].dt.year
    df['quarter'] = df['date_2'].dt.quarter
    list_for_credit_tab_quarter_select_options = list(df['quarter'])
    credit_tab_quarter_select_options = select_options.select_options_func(list_for_credit_tab_quarter_select_options)

    return credit_tab_quarter_select_options