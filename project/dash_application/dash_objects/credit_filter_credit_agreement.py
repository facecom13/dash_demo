import dash_application.functions.df_filter_list as df_filter_list

def credit_filter_credit_agreement_func(df, credit_contract_select):
    full_credit_contract_select_list = list(df['credit_contract'].unique())
    credit_contract_filter_list = df_filter_list.df_filter_list_func(credit_contract_select,
                                                                     full_credit_contract_select_list)
    return credit_contract_filter_list