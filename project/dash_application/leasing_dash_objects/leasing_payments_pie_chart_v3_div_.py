import plotly.graph_objects as go
import dash_application.dash_objects.initial_values as initial_values
from dash import dcc, html
import pandas as pd
import datetime

def leasing_payments_pie_chart_v3_div_func(df_current_agreement_status, data_input, leasing_payments_pie_chart_year_select):
    temp_output = ""
    if data_input == '1с_api':

        df = df_current_agreement_status
        df.sort_values(['date'], inplace=True)

        # фильтр по году
        year_full_list = list(df['year'].unique())
        year_filter = year_full_list
        if leasing_payments_pie_chart_year_select:
            if 'list' in str(type(leasing_payments_pie_chart_year_select)):
                year_filter = leasing_payments_pie_chart_year_select
            else:
                year_filter = list(leasing_payments_pie_chart_year_select)
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



        updated_status_df = df.loc[df['current_agreement_status'].isin(updated_full_agreement_status_list)]

        # определяем даты выборки
        start_date = df.iloc[0]['date']
        finish_date = df.iloc[-1]['date']
        start_month_first_date_str = start_date.strftime("%d.%m.%Y")
        finish_month_first_date_str = finish_date.strftime("%d.%m.%Y")

        finish_year = updated_status_df['year'].max()
        finish_date = datetime.datetime(finish_year, 12, 31)
        period_text = f"Период: с {start_month_first_date_str} по {finish_month_first_date_str}"


        # определяем жирность категорий
        df_categories = updated_status_df.groupby(['current_agreement_status'], as_index=False).agg({'payment_amount': 'sum'})
        df_categories.sort_values(by="payment_amount", ascending=False, inplace=True)
        # df_categories["cumpercentage"] = df_categories["payment_amount"].cumsum() / df_categories['payment_amount'].sum() * 100
        df_categories["share"] = df_categories["payment_amount"] / df_categories['payment_amount'].sum() * 100
        df_categories_magor = df_categories.loc[df_categories['share'] >= 1]
        df_categories_minor = df_categories.loc[df_categories['share'] < 1]

        df_categories_minor_total_sum = df_categories_minor['payment_amount'].sum()
        if df_categories_minor_total_sum > 0:
            added_other_df = pd.DataFrame(
                [{'current_agreement_status': 'Другое', 'payment_amount': df_categories_minor_total_sum}])
            df_categories = pd.concat([df_categories_magor, added_other_df])

        colors_dict = initial_values.colors_dict
        labels = []
        values = []
        colors = []
        i = 0
        for row in df_categories.itertuples():
            category = getattr(row, 'current_agreement_status')
            labels.append(category)
            value = getattr(row, 'payment_amount')
            values.append(value/1000000000)
            colors.append(colors_dict[i])
            i = i + 1

        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            textinfo='percent'
        )])
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.2,
            xanchor="right",
            x=1,

        ))
        # fig.update_layout({
        #     'margin': dict(
        #         # l=2,
        #         r=18,
        #         t=5,
        #         b=5
        #     ),})

        fig.update_traces(
            marker=dict(colors=colors),
            textposition='auto',
            # texttemplate='%{text:.3f} млрд.руб',
            # texttemplate="%{label}: %{value:.3f} <br>(%{percent})"
            # hovertemplate="%{label}: %{value:.3f} млрд.руб <br>(%{percent})"
            hovertemplate="%{label}: %{value:.3f} млрд.руб"

        )

        # temp_df['payment_amount'] = temp_df['payment_amount'].round(decimals =3)
        leasing_payments_piechart_graph = dcc.Graph(
            figure=fig,
            config={'displayModeBar': False},
            style={"height": "100%", "width": "100%"}
        )

        temp_output = period_text
        return [leasing_payments_piechart_graph, temp_output]