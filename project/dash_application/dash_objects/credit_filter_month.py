import dash_application.functions.df_filter_list as df_filter_list

def credit_filter_month_func(df, credit_tab_month_select):
    df = df.copy()
    full_month_select_list = list(df['month'].unique())
    credit_tab_month_select_list = []
    if credit_tab_month_select:
        credit_tab_month_select_value = int(credit_tab_month_select)
        credit_tab_month_select_list.append(credit_tab_month_select_value)
        credit_tab_month_select = credit_tab_month_select_list

    month_filter_list = list(df_filter_list.df_filter_list_func(credit_tab_month_select, full_month_select_list))
    return month_filter_list