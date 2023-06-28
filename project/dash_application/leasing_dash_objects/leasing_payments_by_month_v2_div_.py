import pandas as pd
import dash_application.functions.select_options as select_options
from dash import dcc, html
import plotly.graph_objects as go
import dash_application.dash_objects.initial_values as initial_values

def leasing_payments_by_month_v2_div_func(leasing_df, agreement_status_select_v2, data_input):
    div_output = "leasing_payments_by_month"
    agreement_status_options_select_options = {"1":"1"}
    # обрабатываем полученный df


    df = leasing_df

    # удаляем строки, в которых нет статуса
    df['current_agreement_status'].fillna('delete', inplace=True)
    df = df.loc[~df['current_agreement_status'].isin(['delete', ''])]
    # удаляем строки, в которых нет клиента
    df = df.copy()
    df['customer_name'].fillna('delete', inplace=True)
    df = df.loc[~df['customer_name'].isin(['delete', ''])]

    df['payment_amount'] = df['payment_amount'].astype(float)

    df = df.groupby(['current_agreement_status', 'month_first_date'], as_index=False).agg({'payment_amount': 'sum'})

    # df['date'] = pd.to_datetime(df['date'])
    # try:
    #     df['month_first_date'] = (df['date'].dt.floor('d') + pd.offsets.MonthEnd(0) - pd.offsets.MonthBegin(1))
    # except:
    #     pass
    # df['month_first_date'] = pd.to_datetime(df['month_first_date'])



    full_agreement_status_list = list(df['current_agreement_status'].unique())
    # оставляем только нужные статусы договоров
    updated_full_agreement_status_list = []
    for agreement_status in full_agreement_status_list:
        if 'действует' in agreement_status.lower() or 'подписан' in agreement_status.lower():
            updated_full_agreement_status_list.append(agreement_status)

    # agreement_status_options_select_options = select_options.select_options_func(updated_full_agreement_status_list)

    updated_status_df = df.loc[df['current_agreement_status'].isin(updated_full_agreement_status_list)]

    agreement_status_filter = updated_full_agreement_status_list
    # if agreement_status_select_v2:
    #     if 'list' in (str(type(agreement_status_select_v2))):
    #         agreement_status_filter = agreement_status_select_v2
    #     else:
    #         agreement_status_filter = []
    #         agreement_status_filter.append(agreement_status_select_v2)

    # df_fig = updated_status_df.loc[updated_status_df['current_agreement_status'].isin(agreement_status_filter)]

    # df_fig.sort_values(by="month_first_date", inplace=True)

    df_fig = updated_status_df

    # определяем жирность категорий
    df_categories = df_fig.groupby(['current_agreement_status'], as_index=False).agg({'payment_amount': 'sum'})
    df_categories.sort_values(by="payment_amount", ascending=False, inplace=True)
    agreement_status_list = list(df_categories['current_agreement_status'].unique())

    fig = go.Figure()

    i = 0

    colors_dict = initial_values.colors_dict
    df['payment_amount'] = df['payment_amount'].astype(float)

    for agreement_status in agreement_status_list:
        temp_df = df.loc[df['current_agreement_status'] == agreement_status]
        temp_df = temp_df.copy()
        # temp_df['payment_amount'] = temp_df['payment_amount']/1000000000

        # temp_df['payment_amount'] = temp_df['payment_amount'].round(decimals =3)

        x = list(temp_df['month_first_date'])

        y = list(temp_df['payment_amount'])

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


    div_output = html.Div(
        children=[
            leasing_payments_by_month_graph
        ]
    )


    return div_output, agreement_status_options_select_options

