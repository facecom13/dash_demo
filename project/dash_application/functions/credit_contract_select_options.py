import dash_application.functions.select_options as select_options
def credit_contract_select_options_func(df, creditor_select):
    if creditor_select:
        df = df.loc[df['creditor'].isin(creditor_select)]
    list_for_credit_contract_select_options = list(df['credit_contract'])
    credit_contract_select_options = select_options.select_options_func(list_for_credit_contract_select_options)
    return credit_contract_select_options