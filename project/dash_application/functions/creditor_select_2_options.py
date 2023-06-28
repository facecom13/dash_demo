import dash_application.functions.select_options as select_options

def creditor_select_2_options_func(df):
    list_for_creditor_select_options = list(df['creditor'].unique())
    creditor_select_options = select_options.select_options_func(list_for_creditor_select_options)
    return creditor_select_options