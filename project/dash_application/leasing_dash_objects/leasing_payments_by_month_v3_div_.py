import datetime
import os
import plotly.graph_objects as go
import dash_application.dash_objects.initial_values as initial_values
from dash import dcc, html
from sqlalchemy import create_engine
def leasing_payments_by_month_v3_div_func(df, data_input, leasing_payments_by_month_year_select):
    output = ''
    if data_input =='1с_api':
        df.sort_values(['date'], inplace=True)
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

        # определяем даты выборки

        start_year = updated_status_df['year'].min()
        # start_date = datetime.datetime(start_year, 1,1)
        start_date = df.iloc[0]['date']
        finish_date = df.iloc[-1]['date']
        start_month_first_date_str = start_date.strftime("%d.%m.%Y")
        finish_month_first_date_str = finish_date.strftime("%d.%m.%Y")
        finish_year = updated_status_df['year'].max()
        # finish_date = datetime.datetime(finish_year, 12,31)




        period_text = f"Период: с {start_month_first_date_str} по {finish_month_first_date_str}"

        # схлопываем df для построения графика
        df_fig = updated_status_df.groupby(['current_agreement_status', 'month_first_date'], as_index=False).agg({'payment_amount': 'sum'})
        # определяем жирность категорий
        df_categories = df_fig.groupby(['current_agreement_status'], as_index=False).agg({'payment_amount': 'sum'})
        df_categories.sort_values(by="payment_amount", ascending=False, inplace=True)
        agreement_status_list = list(df_categories['current_agreement_status'].unique())

        colors_dict = initial_values.colors_dict

        fig = go.Figure()

        i = 0

        for agreement_status in agreement_status_list:
            temp_df = df_fig.loc[df_fig['current_agreement_status'] == agreement_status]
            temp_df = temp_df.copy()
            # temp_df['payment_amount'] = temp_df['payment_amount']/1000000000

            # temp_df['payment_amount'] = temp_df['payment_amount'].round(decimals =3)

            x = list(temp_df['month_first_date'])

            y = list(temp_df['payment_amount']/1000000000)

            trace_color = "#E8E8E8"
            try:
                trace_color = colors_dict[i]
            except:
                pass

            fig.add_trace(go.Bar(
                x=x,
                y=y,
                name=agreement_status,
                marker={'color': trace_color},
                # hovertemplate='%{x}: %{y} руб<extra></extra>',
            ))

            i = i + 1

        fig.update_layout({
            'barmode': 'stack',
            'xaxis_tickangle': -90,
            'margin': dict(l=2, r=18, t=5, b=5),

            # "title": "Погашение кредитного портфеля",
            'legend': {
                'orientation': "h",
                'yanchor': "bottom",
                'y': 1.08,
            }
        })

        fig.update_traces(
            # textposition='auto',
            # texttemplate='%{text:.3f} млрд.руб',
            # texttemplate="%{label}: %{value:.3f} <br>(%{percent})"
            # hovertemplate="%{label}: %{value:.3f} млрд.руб <br>(%{percent})"
            hovertemplate="%{label}: %{value:.3f} млрд.руб"

        )



        leasing_payments_by_month_graph = dcc.Graph(figure=fig, config={'displayModeBar': False})

        div_output = html.Div(
            children=[
                leasing_payments_by_month_graph
            ]
        )
        return div_output, period_text
