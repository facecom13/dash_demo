import dash_application.functions.select_options as select_options
import pandas as pd
def taken_tranch_year_select_options_func(df):
    df['credit_tranch_date_2'] = pd.to_datetime(df['credit_tranch_date'])
    if "int" in str(df['credit_tranch_date'].dtype):
        df['credit_tranch_date_2'] = pd.to_datetime(df['credit_tranch_date'], unit='ms')

    df['tranch_year'] = df['credit_tranch_date_2'].dt.year
    # print(df.loc[:, ['credit_tranch_date', 'tranch_year']])
    list_for_credit_tab_tranch_year_select_options = list(df['tranch_year'])
    taken_tranch_year_select_options = select_options.select_options_func(
        list_for_credit_tab_tranch_year_select_options)

    return taken_tranch_year_select_options