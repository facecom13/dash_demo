import dash_application.functions.df_filter_list as df_filter_list

def credit_filters_func(df, creditor_select):
    full_creditor_select_list = list(df['creditor'].unique())
    creditor_filter_list = df_filter_list.df_filter_list_func(creditor_select, full_creditor_select_list)
    return creditor_filter_list