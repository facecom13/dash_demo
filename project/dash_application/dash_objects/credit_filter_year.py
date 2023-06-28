import dash_application.functions.df_filter_list as df_filter_list

def credit_filter_year_func(df, tab_1_year_select):
    df = df.loc[df['year']>=2023]
    full_year_select_list = list(df['year'].unique())
    tab_1_year_select_list = []
    if tab_1_year_select:
        tab_1_year_select_value = int(tab_1_year_select)
        tab_1_year_select_list.append(tab_1_year_select_value)
        tab_1_year_select = tab_1_year_select_list

    year_filter_list = list(df_filter_list.df_filter_list_func(tab_1_year_select, full_year_select_list))
    return year_filter_list