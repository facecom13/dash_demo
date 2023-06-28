from dash import dcc
import psycopg2
import plotly.graph_objects as go
import os
from sqlalchemy import create_engine
import pandas as pd
import datetime
def leasing_object_type_barchart_div_func(df, data_input, leasing_object_type_year_select):
    output = 'leasing_object_type_barchart_div_func'
    period_text = ""
    if data_input == '1с_api':
        df.sort_values(['date'], inplace=True)


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
        output_div = "no data"
        if len(df)>0:
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

            df['leasing_object_type'].fillna('no_data')
            df_fig = df
            df_fig['leasing_object_type'] = df_fig['leasing_object_type'].str.replace(r'^\s*$', 'no_data', regex=True)
            df_fig = df_fig.copy()
            df_fig = df_fig.loc[df['leasing_object_type'] != 'no_data']

            df_leasing_object_type = df_fig.groupby(['leasing_object_type'], as_index=False).agg(
                {'payment_amount': 'sum'})

            df_leasing_object_type.sort_values(by="payment_amount", ascending=False, inplace=True)

            df_leasing_object_type = df_leasing_object_type.head(20)
            df_leasing_object_type.sort_values(["payment_amount"], ascending=True, inplace=True)

            df_leasing_object_type['payment_amount'] = df_leasing_object_type['payment_amount'] / 1000000000
            df_leasing_object_type['payment_amount'] = df_leasing_object_type['payment_amount'].round(decimals=3)

            payment_amount_list = list(df_leasing_object_type['payment_amount'])
            df_leasing_object_type_list = list(df_leasing_object_type['leasing_object_type'])
            payment_amount_max_value = max(payment_amount_list) * 1.02
            payment_amount_min_value = min(payment_amount_list) - min(payment_amount_list) * 0.3

            fig = go.Figure(go.Bar(
                x=payment_amount_list,
                y=df_leasing_object_type_list,
                text=payment_amount_list,
                marker={"color": '#b27aa1'},
                orientation='h',
                name="",
                textposition='auto'
            ))
            fig.update_xaxes(range=[payment_amount_min_value, payment_amount_max_value])
            fig.update_layout({
                'margin': dict(l=5, r=5, t=5, b=5),
                # "title": "Средневзвешенная ставка",
            })

            fig.update_traces(
                texttemplate='%{text:.3f} млрд руб.',
                hovertemplate='%{y}: %{text:.3f} млрд руб.'
            )

            output_div = dcc.Graph(config={'displayModeBar': False}, figure=fig)


        output = output_div

    return output, period_text