import dash_application.functions.df_filter_list as df_filter_list

def credit_filter_quarter_func(df, tab_1_quarter_select):
    full_quarter_select_list = list(df['quarter'].unique())
    tab_1_quarter_select_list = []
    if tab_1_quarter_select:
        tab_1_quarter_select_value = int(tab_1_quarter_select)
        tab_1_quarter_select_list.append(tab_1_quarter_select_value)
        tab_1_quarter_select = tab_1_quarter_select_list

    quarter_filter_list = list(df_filter_list.df_filter_list_func(tab_1_quarter_select, full_quarter_select_list))
    return quarter_filter_list