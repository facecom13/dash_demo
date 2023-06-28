from dash import dcc, html
import plotly.graph_objects as go
import plotly.express as px
import datetime
import dash_application.dash_objects.initial_values as initial_values
from dash import dash_table
import pandas as pd
def leasing_payments_by_month_graph_div_func(leasing_payment_graph_df, agreement_status_select):

    full_agreement_status_select = list(leasing_payment_graph_df['current_agreement_status'].unique())
    agreement_status_filter = full_agreement_status_select
    if agreement_status_select:
        if 'list' in (str(type(agreement_status_select))):
            agreement_status_filter = agreement_status_select
        else:
            agreement_status_filter = []
            agreement_status_filter.append(agreement_status_select)

    df = leasing_payment_graph_df.loc[leasing_payment_graph_df['current_agreement_status'].isin(agreement_status_filter)]
    df.sort_values(by="month_first_date", inplace=True)

    # определяем жирность категорий
    df_categories = df.groupby(['current_agreement_status'],as_index=False).agg({'payment_amount': 'sum'})
    df_categories.sort_values(by="payment_amount", ascending=False, inplace=True)
    # итерируемся по категориям и присваиваем им цвета
    agreement_status_list = list(df_categories['current_agreement_status'].unique())


    fig = go.Figure()
    # получаем список категорий
    # agreement_status_list = list(df['current_agreement_status'].unique())
    # colors = ["#FFC000", "#32935F"]

    i = 0
    # colors = px.colors.sequential.Plasma
    colors = ["#E8E8E8","#b3e5ca", "#FFC000", "#909090", "#32935F", '#FEFBE9', '#E1EEDD', '#F0A04B', '#183A1D', '#698269', '#B99B6B,' '#AA5656', '#678983', '#FFB100', '#658864', '#B7B78A', '#815B5B', '#5D3891', '#5D3891', '#86E5FF', '#A555EC', '#0F6292', '#FFED00']
    colors_dict = initial_values.colors_dict

    for agreement_status in agreement_status_list:
        # if agreement_status == 'Действует':
        temp_df = df.loc[df['current_agreement_status'] == agreement_status]
        temp_df = temp_df.copy()
        # temp_df['payment_amount'] = temp_df['payment_amount']/1000000000
        # temp_df['payment_amount'] = temp_df['payment_amount']
        temp_df['payment_amount'] = temp_df['payment_amount'].round(decimals =3)

        x = list(temp_df['month_first_date'])
        # print("x_credit: ", x_credit)
        y = list(temp_df['payment_amount'])
        # return str(x) + str(y)
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
        i=i+1


    date_start = initial_values.start_date
    date_finish = initial_values.finish_date
    # добавление вертикальных линий в первый день года
    # first_year_date_start = datetime.datetime(date_start.year, 1, 1)
    # temp_date = first_year_date_start
    # while temp_date < date_finish:
    #     fig.add_vline(
    #         x=temp_date,
    #         # line_width=3,
    #         # line_dash="dash",
    #         line_color="grey")
    #     temp_date = temp_date + datetime.timedelta(days=365.25)

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

    leasing_payments_by_month_graph = dcc.Graph(figure=fig, config={'displayModeBar': False})

    data = df.to_dict('records')
    credit_datatable = dash_table.DataTable(
        data=data,)

    leasing_payments_by_month_ = html.Div(
        children=[
            leasing_payments_by_month_graph,
            # credit_datatable
        ]
    )
    # return str(fig)
    return leasing_payments_by_month_
    # return credit_datatable
    # return str(df.info())