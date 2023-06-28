import dash_application.functions.select_options as select_options
def taken_tranch_creditor_select_v2_options_func(df, taken_tranch_year_select_value_, taken_tranch_year_select_value):

    tranch_year_filter_value = int(taken_tranch_year_select_value_)
    if taken_tranch_year_select_value:
        tranch_year_filter_value = int(taken_tranch_year_select_value)

    df = df.loc[df['tranch_year'] == tranch_year_filter_value]
    list_for_creditor_select_options = list(df['creditor'].unique())
    creditor_select_options = select_options.select_options_func(list_for_creditor_select_options)

    return creditor_select_options