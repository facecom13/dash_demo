

def leasing_payments_by_month_download_func(df, data_input, leasing_payments_by_month_year_select):
    if data_input == '1с_api':
        # удаляем ненужные статусы
        full_agreement_status_list = list(df['current_agreement_status'].unique())
        # оставляем только нужные статусы договоров
        updated_full_agreement_status_list = []
        for agreement_status in full_agreement_status_list:
            if 'действует' in agreement_status.lower() or 'подписан' in agreement_status.lower():
                updated_full_agreement_status_list.append(agreement_status)

        # agreement_status_options_select_options = select_options.select_options_func(updated_full_agreement_status_list)

        # фильтр по году
        year_full_list = list(df['year'].unique())
        year_filter = year_full_list
        if leasing_payments_by_month_year_select:
            if 'list' in str(type(leasing_payments_by_month_year_select)):
                year_filter = leasing_payments_by_month_year_select
            else:
                year_filter = list(leasing_payments_by_month_year_select)
        year_filter_int_list = []
        for year in year_filter:
            year = int(year)
            year_filter_int_list.append(year)

        # режем выборку по году
        df = df.loc[df['year'].isin(year_filter_int_list)]

        updated_status_df = df.loc[df['current_agreement_status'].isin(updated_full_agreement_status_list)]

        return updated_status_df