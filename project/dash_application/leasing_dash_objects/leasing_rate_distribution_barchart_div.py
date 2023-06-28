from dash import dcc
import psycopg2
import plotly.graph_objects as go
import os
from sqlalchemy import create_engine
import pandas as pd
import datetime
def leasing_rate_distribution_barchart_div_func(df, data_input, leasing_rate_distribution_barchart_year_select):
    output = 'leasing_products_barchart_div_func'
    period_text = ""
    if data_input == '1с_api':
        df.sort_values(['date'], inplace=True)

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

        # определяем даты выборки
        start_date = df.iloc[0]['date']
        # finish_date = df.iloc[-1]['date']
        # start_date = datetime.datetime(start_year, 1, 1)
        start_month_first_date_str = start_date.strftime("%d.%m.%Y")
        # finish_year = df_fig['year'].max()
        finish_date = df.iloc[-1]['date']
        # finish_date = datetime.datetime(finish_year, 12, 31)
        finish_month_first_date_str = finish_date.strftime("%d.%m.%Y")
        period_text = f"Период: с {start_month_first_date_str} по {finish_month_first_date_str}"

        df = df.copy()
        less_5_df = df.loc[df['leasing_rate']<5]
        more_5_df = df.loc[df['leasing_rate']>=5]
        more_5_df_less_8_df = more_5_df.loc[more_5_df['leasing_rate']<8]
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
        more_13_df['sort_index']  = 6

        df = pd.concat([less_5_df, more_5_df_less_8_df, more_8_df_less_10_df, more_10_df_less_12_df, more_12_df_less_13_df, more_13_df])



        df_rate_category = df.groupby(['rate_category', 'sort_index'], as_index=False).agg(
            {'payment_amount': 'sum'})

        df_rate_category.sort_values(['sort_index'], inplace=True)

        df_rate_category['payment_amount'] = df_rate_category['payment_amount'] / 1000000000
        df_rate_category['rate_category'].astype('category')


        payment_amount_list = df_rate_category['payment_amount']
        rate_category_list = df_rate_category['rate_category']
        payment_amount_max_value = max(payment_amount_list) * 1.1
        payment_amount_min_value = min(payment_amount_list) - min(payment_amount_list) * 0.3


        fig = go.Figure(go.Bar(
            y=payment_amount_list,
            x=rate_category_list,
            text=payment_amount_list,
            marker={"color": '#678983'},
            # orientation='h',
            # name="",
            textposition='auto'
        ))
        fig.update_yaxes(range=[0, payment_amount_max_value])
        fig.update_layout({
            'margin': dict(l=5, r=5, t=5, b=5),
            # "title": "Средневзвешенная ставка",
        })

        fig.update_traces(
            texttemplate='%{text:.3f}',
            hovertemplate='%{y}: %{text:.3f} млрд.руб'
        )

        output_div = dcc.Graph(config={'displayModeBar': False}, figure=fig)


        output = output_div

    return output, period_text