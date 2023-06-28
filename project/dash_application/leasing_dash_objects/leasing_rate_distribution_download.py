import pandas as pd

def leasing_rate_distribution_download_download_func(df, data_input, leasing_rate_distribution_barchart_year_select):
    if data_input == '1с_api':
        # фильтр по году
        year_full_list = list(df['year'].unique())
        year_filter = year_full_list
        if leasing_rate_distribution_barchart_year_select:
            if 'list' in str(type(leasing_rate_distribution_barchart_year_select)):
                year_filter = leasing_rate_distribution_barchart_year_select
            else:
                year_filter = list(leasing_rate_distribution_barchart_year_select)
        year_filter_int_list = []
        for year in year_filter:
            year = int(year)
            year_filter_int_list.append(year)

        # режем выборку по году
        df = df.loc[df['year'].isin(year_filter_int_list)]

        df = df.copy()
        less_5_df = df.loc[df['leasing_rate'] < 5]
        more_5_df = df.loc[df['leasing_rate'] >= 5]
        more_5_df_less_8_df = more_5_df.loc[more_5_df['leasing_rate'] < 8]
        more_8_df = df.loc[df['leasing_rate'] >= 8]
        more_8_df_less_10_df = more_8_df.loc[more_8_df['leasing_rate'] < 10]
        more_10_df = df.loc[df['leasing_rate'] >= 10]
        more_10_df_less_12_df = more_10_df.loc[more_10_df['leasing_rate'] < 12]
        more_12_df = df.loc[df['leasing_rate'] >= 12]
        more_12_df_less_13_df = more_12_df.loc[more_12_df['leasing_rate'] < 13]
        more_13_df = df.loc[df['leasing_rate'] >= 13]

        less_5_df = less_5_df.copy()
        less_5_df['rate_category'] = '<5'
        less_5_df['sort_index'] = 1

        more_5_df_less_8_df = more_5_df_less_8_df.copy()
        more_5_df_less_8_df['rate_category'] = '>=5<8'
        more_5_df_less_8_df['sort_index'] = 2

        more_8_df_less_10_df = more_8_df_less_10_df.copy()
        more_8_df_less_10_df['rate_category'] = '>=8<10'
        more_8_df_less_10_df['sort_index'] = 3

        more_10_df_less_12_df = more_10_df_less_12_df.copy()
        more_10_df_less_12_df['rate_category'] = '>=10<12'
        more_10_df_less_12_df['sort_index'] = 4

        more_12_df_less_13_df = more_12_df_less_13_df.copy()
        more_12_df_less_13_df['rate_category'] = '>=12<13'
        more_12_df_less_13_df['sort_index'] = 5

        more_13_df = more_13_df.copy()
        more_13_df['rate_category'] = '>=13'
        more_13_df['sort_index'] = 6

        df = pd.concat(
            [less_5_df, more_5_df_less_8_df, more_8_df_less_10_df, more_10_df_less_12_df, more_12_df_less_13_df,
             more_13_df])


        return df