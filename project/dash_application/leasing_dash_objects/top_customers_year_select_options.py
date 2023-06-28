import dash_application.functions.select_options as select_options

def top_customers_year_select_options_func(df_leasing_payment_graph):
    top_customers_year_select_options = {2023:2023}
    try:
        full_year_list = list(df_leasing_payment_graph['year'].unique())
        full_year_list_converted = []
        for year in full_year_list:
            year = int(year)
            full_year_list_converted.append(year)
        top_customers_year_select_options = select_options.select_options_func(full_year_list_converted)
    except Exception as e:
        print(e)
    return top_customers_year_select_options