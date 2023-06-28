import dash_application.functions.select_options as select_options

def agreement_status_select_options_func(df_leasing_payment_graph):

    full_agreement_status_list = list(df_leasing_payment_graph['current_agreement_status'].unique())
    agreement_status_options_select_options = select_options.select_options_func(full_agreement_status_list)
    return agreement_status_options_select_options
