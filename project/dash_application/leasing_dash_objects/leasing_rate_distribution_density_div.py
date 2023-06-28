import pandas as pd
import datetime
import plotly.graph_objects as go
from dash import dcc

def leasing_rate_distribution_density_div_func(df, data_input, leasing_rate_distribution_density_year_select):
    output = 'leasing_products_barchart_div_func'
    period_text = ""
    if data_input == '1с_api':

        # фильтр по году
        year_full_list = list(df['year'].unique())
        year_filter = year_full_list
        if leasing_rate_distribution_density_year_select:
            if 'list' in str(type(leasing_rate_distribution_density_year_select)):
                year_filter = leasing_rate_distribution_density_year_select
            else:
                year_filter = list(leasing_rate_distribution_density_year_select)
        year_filter_int_list = []
        for year in year_filter:
            year = int(year)
            year_filter_int_list.append(year)

        # режем выборку по году
        df = df.loc[df['year'].isin(year_filter_int_list)]



        # определяем даты выборки
        start_year = df['year'].min()
        start_date = datetime.datetime(start_year, 1, 1)
        start_month_first_date_str = start_date.strftime("%d.%m.%Y")
        finish_year = df['year'].max()
        finish_date = datetime.datetime(finish_year, 12, 31)
        finish_month_first_date_str = finish_date.strftime("%d.%m.%Y")
        period_text = f"Период: с {start_month_first_date_str} по {finish_month_first_date_str}"

        df = df.copy()

        df_rate_density = df.groupby(['leasing_rate'], as_index=False).agg(
            {'leasing_rate_count': 'count'})


        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_rate_density['leasing_rate'],
            y=df_rate_density['leasing_rate_count'],
            fill='tozeroy'))  # fill down to xaxis

        fig.update_layout({
            'margin': dict(l=5, r=5, t=5, b=5),
            # "title": "Средневзвешенная ставка",
        })

        output_div = dcc.Graph(config={'displayModeBar': False}, figure=fig)
        output =output_div




    return output, period_text