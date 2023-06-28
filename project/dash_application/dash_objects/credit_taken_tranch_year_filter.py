import dash_application.functions.df_filter_list as df_filter_list

def credit_taken_tranch_year_filter_func(df, taken_tranch_year_select):
    full_year_select_list = list(df['year'].unique())

    taken_tranch_year_select_list = []
    if taken_tranch_year_select:
        taken_tranch_year_select_value = int(taken_tranch_year_select)
        taken_tranch_year_select_list.append(taken_tranch_year_select_value)


    year_filter_list = list(df_filter_list.df_filter_list_func(taken_tranch_year_select_list, full_year_select_list))
    return year_filter_list