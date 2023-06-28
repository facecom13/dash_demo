from dash import dcc
import psycopg2
import plotly.graph_objects as go
import os
from sqlalchemy import create_engine
import pandas as pd
import datetime
def leasing_rate_barchart_div_func(df, data_input, leasing_rate_year_select):
    output = 'leasing_rate_barchart_div_func'
    period_text = ""
    if data_input == '1с_api':
        df.sort_values(['date'], inplace=True)


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



        df['leasing_product'].fillna('no_data')
        df_fig = df
        df_fig['leasing_product'] = df_fig['leasing_product'].str.replace(r'^\s*$', 'no_data', regex=True)
        df_fig = df_fig.copy()
        df_fig = df_fig.loc[df['leasing_product'] != 'no_data']

        df_leasing_rate = df_fig
        df_leasing_rate['percent_amount'] = df_leasing_rate['payment_amount'] * (df_leasing_rate['leasing_rate'] /100 )

        # Получаем список leasing_product
        leasing_product_list = list(df_leasing_rate['leasing_product'].unique())

        # итерируемся по списку продуктов
        leasing_product_rate_result_list = []

        for leasing_product in leasing_product_list:
            temp_dict = {}
            temp_df = df_leasing_rate.loc[df_leasing_rate['leasing_product']==leasing_product]
            temp_df_groupped = temp_df.groupby(['leasing_product'], as_index=False).agg({'payment_amount': 'sum', 'percent_amount': 'sum'})

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

        x_axis = common_df['leasing_product']
        y_axis = common_df['leasing_product_rate']

        leasing_product_list = list(common_df['leasing_product'])

        i = 0
        total_ave_rate_index = 0
        for creditor in leasing_product_list:
            if creditor == "По портфелю":
                total_ave_rate_index = i
            i = i + 1

        colors = ['#32935F', ] * len(leasing_product_list)
        colors[total_ave_rate_index] = '#FFC000'

        ave_max_value = max(y_axis) * 1.05
        ave_rate_min_value = min(y_axis) - min(y_axis) * 0.15



        fig_leasing_product_rate = go.Figure(go.Bar(
            y=x_axis,
            x=y_axis,
            text=y_axis,
            marker={"color": colors},
            orientation='h',
            name="",
            textposition='auto'
        ))

        fig_leasing_product_rate.update_xaxes(range=[ave_rate_min_value, ave_max_value])
        fig_leasing_product_rate.update_layout({
            'margin': dict(l=5, r=5, t=5, b=5),
            # "title": "Средневзвешенная ставка",
        })

        fig_leasing_product_rate.update_traces(
            texttemplate='%{text:.2f}%',
            # texttemplate='%{x}%',
            hovertemplate='%{y}: %{text:.2f}%'
        )



        output_div = dcc.Graph(config={'displayModeBar': False}, figure=fig_leasing_product_rate)




        output = output_div

    return output, period_text