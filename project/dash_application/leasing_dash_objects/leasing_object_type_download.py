

def leasing_object_type_download_func(df, data_input, leasing_object_type_year_select):
    if data_input == '1с_api':
        # фильтр по году
        year_full_list = list(df['year'].unique())
        year_filter = year_full_list
        if leasing_object_type_year_select:
            if 'list' in str(type(leasing_object_type_year_select)):
                year_filter = leasing_object_type_year_select
            else:
                year_filter = list(leasing_object_type_year_select)
        year_filter_int_list = []
        for year in year_filter:
            year = int(year)
            year_filter_int_list.append(year)

        # режем выборку по году
        df = df.loc[df['year'].isin(year_filter_int_list)]

        updated_status_df =df.groupby(['leasing_object_type', 'year'], as_index=False).agg(
            {'payment_amount': 'sum'})


        return updated_status_df