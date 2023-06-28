import pandas as pd

def leasing_rate_download_download_func(df, data_input, leasing_rate_year_select):
    if data_input == '1с_api':
        # фильтр по году
        year_full_list = list(df['year'].unique())
        year_filter = year_full_list
        if leasing_rate_year_select:
            if 'list' in str(type(leasing_rate_year_select)):
                year_filter = leasing_rate_year_select
            else:
                year_filter = list(leasing_rate_year_select)
        year_filter_int_list = []
        for year in year_filter:
            year = int(year)
            year_filter_int_list.append(year)

        # режем выборку по году
        df = df.loc[df['year'].isin(year_filter_int_list)]

        df['leasing_product'].fillna('no_data')
        df_fig = df
        df_fig['leasing_product'] = df_fig['leasing_product'].str.replace(r'^\s*$', 'no_data', regex=True)
        df_fig = df_fig.copy()
        df_fig = df_fig.loc[df['leasing_product'] != 'no_data']

        df_leasing_rate = df_fig
        df_leasing_rate['percent_amount'] = df_leasing_rate['payment_amount'] * (df_leasing_rate['leasing_rate'] / 100)

        # Получаем список leasing_product
        leasing_product_list = list(df_leasing_rate['leasing_product'].unique())

        # итерируемся по списку продуктов
        leasing_product_rate_result_list = []

        for leasing_product in leasing_product_list:
            temp_dict = {}
            temp_df = df_leasing_rate.loc[df_leasing_rate['leasing_product'] == leasing_product]
            temp_df_groupped = temp_df.groupby(['leasing_product'], as_index=False).agg(
                {'payment_amount': 'sum', 'percent_amount': 'sum'})

            # Сумма лизинговых платежей в получившейся выборке
            payment_amount_sum = temp_df_groupped['payment_amount'].sum()

            # сумма процентов в получившейся выборке =
            percent_amount_sum = temp_df_groupped['percent_amount'].sum()

            # процентная ставка в получившейся выборке
            leasing_product_rate = percent_amount_sum / payment_amount_sum * 100

            temp_dict['leasing_product'] = leasing_product
            temp_dict['leasing_product_rate'] = leasing_product_rate

            leasing_product_rate_result_list.append(temp_dict)

        leasing_product_rate_df = pd.DataFrame(leasing_product_rate_result_list)

        leasing_product_rate_df.sort_values(by=['leasing_product_rate'], inplace=True)

        # считаем по портфелю
        total_leasing_payment_amount = df_leasing_rate['payment_amount'].sum()
        total_leasing_percent_amount = df_leasing_rate['percent_amount'].sum()
        total_leasing_product_rate = total_leasing_percent_amount / total_leasing_payment_amount * 100

        df1 = pd.DataFrame([{"leasing_product": "По портфелю", "leasing_product_rate": total_leasing_product_rate}])
        common_df = pd.concat([leasing_product_rate_df, df1])





        return common_df