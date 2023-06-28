import dash_application.functions.mapping as mapping

import pandas as pd
def credit_tab_month_select_options_func(df, credit_tab_quarter_select_value):
    df['date_2'] = pd.to_datetime(df['date'])
    if "int" in str(df['date'].dtype):
        df['date_2'] = pd.to_datetime(df['date'], unit='ms')
    df['year'] = df['date_2'].dt.year
    df['quarter'] = df['date_2'].dt.quarter
    df['month'] = df['date_2'].dt.month

    list_for_credit_tab_month_select_options = list(df['month'])
    # credit_tab_month_select_options = select_options.select_options_func(list_for_credit_tab_month_select_options)
    unique_list = set(list_for_credit_tab_month_select_options)
    options_dict = {}
    month_mapping_dict = mapping.month_mapping()

    for item in unique_list:
        options_dict[item] = month_mapping_dict[item]

    return options_dict
