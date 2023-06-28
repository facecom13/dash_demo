import pandas as pd
from dash import dcc
import plotly.graph_objects as go
import dash_application.dash_objects.initial_values as initial_values
import datetime

def top_group_customers_barchart_v2__div_func(df, data_input, top_customers_year_select):
    if data_input == '1с_api':
        df.sort_values(['date'], inplace=True)
        # фильтр по году
        year_full_list = list(df['year'].unique())
        year_filter = year_full_list
        if top_customers_year_select:
            if 'list' in str(type(top_customers_year_select)):
                year_filter = top_customers_year_select
            else:
                year_filter = list(top_customers_year_select)
        year_filter_int_list = []
        for year in year_filter:
            year = int(year)
            year_filter_int_list.append(year)

        # режем выборку по году
        df = df.loc[df['year'].isin(year_filter_int_list)]



        # удаляем ненужные статусы
        full_agreement_status_list = list(df['current_agreement_status'].unique())
        # оставляем только нужные статусы договоров
        updated_full_agreement_status_list = []
        for agreement_status in full_agreement_status_list:
            if 'действует' in agreement_status.lower() or 'подписан' in agreement_status.lower():
                updated_full_agreement_status_list.append(agreement_status)

        # agreement_status_options_select_options = select_options.select_options_func(updated_full_agreement_status_list)

        updated_status_df = df.loc[df['current_agreement_status'].isin(updated_full_agreement_status_list)]



        # схлопываем df для построения графика
        # df_fig = updated_status_df.groupby(['company_group', 'year', 'current_agreement_status', 'month_first_date'], as_index=False).agg(
        #     {'payment_amount': 'sum'})
        updated_status_df = updated_status_df.copy()
        # Заполняем колонку company_group
        updated_status_df['company_group'].fillna('no_data', inplace=True)
        df_fig = updated_status_df
        df_fig = df_fig.copy()
        df_fig['company_group'] = df_fig['company_group'].str.replace(r'^\s*$', 'no_data', regex=True)
        df_fig = df_fig.loc[df_fig['company_group'] != 'no_data']

        # определяем даты выборки
        start_date = df_fig.iloc[0]['date']
        # finish_date = df.iloc[-1]['date']
        # start_date = datetime.datetime(start_year, 1, 1)
        start_month_first_date_str = start_date.strftime("%d.%m.%Y")
        finish_year = updated_status_df['year'].max()
        finish_date = df_fig.iloc[-1]['date']
        # finish_date = datetime.datetime(finish_year, 12, 31)
        finish_month_first_date_str = finish_date.strftime("%d.%m.%Y")
        period_text = f"Период: с {start_month_first_date_str} по {finish_month_first_date_str}"




        df_company_group = df_fig.groupby(['company_group'], as_index=False).agg(
            {'payment_amount': 'sum'})

        df_company_group.sort_values(by="payment_amount",ascending=False, inplace=True)
        df_company_group = df_company_group.head(20)
        df_company_group.sort_values(by="payment_amount", ascending=True, inplace=True)

        payment_amount_list = list(df_company_group['payment_amount']/1000000000)
        company_group_list = list(df_company_group['company_group'])
        payment_amount_max_value = max(payment_amount_list) * 1.5
        payment_amount_min_value = min(payment_amount_list) - min(payment_amount_list) * 0.3

        fig = go.Figure(go.Bar(
            x=payment_amount_list,
            y=company_group_list,
            text=payment_amount_list,
            marker={"color": '#32935F'},
            orientation='h',
            name="",
            textposition='outside'
        ))
        fig.update_xaxes(range=[payment_amount_min_value, payment_amount_max_value])
        fig.update_layout({
            'margin': dict(l=5, r=5, t=5, b=5),
            # "title": "Средневзвешенная ставка",
        })

        fig.update_traces(
            texttemplate='%{text:.3f} млрд.руб',
            hovertemplate='%{y}: %{text:.3f} млрд.руб',
            textfont_size=14
        )


        output_div = dcc.Graph(config={'displayModeBar': False}, figure=fig)


        return output_div, period_text

