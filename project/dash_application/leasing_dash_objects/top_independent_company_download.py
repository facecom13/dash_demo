

def top_independent_company_download_func(df, data_input, top_independent_customers_year_select):
    if data_input == '1с_api':
        # фильтр по году
        year_full_list = list(df['year'].unique())
        year_filter = year_full_list
        if top_independent_customers_year_select:
            if 'list' in str(type(top_independent_customers_year_select)):
                year_filter = top_independent_customers_year_select
            else:
                year_filter = list(top_independent_customers_year_select)
        year_filter_int_list = []
        for year in year_filter:
            year = int(year)
            year_filter_int_list.append(year)

        # режем выборку по году
        df = df.loc[df['year'].isin(year_filter_int_list)]

        updated_status_df =df.groupby(['customer_name', 'year'], as_index=False).agg(
            {'payment_amount': 'sum'})

        updated_status_df.sort_values(["payment_amount"], ascending=False, inplace=True)

        return updated_status_df