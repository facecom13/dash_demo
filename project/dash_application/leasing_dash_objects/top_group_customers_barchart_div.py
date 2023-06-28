from dash import dcc, html
import plotly.graph_objects as go
import plotly.express as px
import datetime
import dash_application.dash_objects.initial_values as initial_values
from dash import dash_table
import pandas as pd
def top_group_customers_barchart_div_func(leasing_data_df, top_customers_year_select):
    full_top_customers_year = list(leasing_data_df['year'].unique())
    year_filter = full_top_customers_year
    if top_customers_year_select:
        if 'list' in (str(type(top_customers_year_select))):
            year_filter = top_customers_year_select
        else:
            year_filter = []
            year_filter.append(top_customers_year_select)
    year_select_list = []
    for year in year_filter:
        year  = int(year)
        year_select_list.append(year)

    df = leasing_data_df.loc[
        leasing_data_df['year'].isin(year_select_list)]
    # Заполняем колонку company_group
    df['company_group'].fillna('no_data')
    df = df.copy()
    df['company_group'] = df['company_group'].str.replace(r'^\s*$', 'no_data', regex=True)

    # получаем df с company_group
    df_company_group = df.loc[df['company_group']!='no_data']
    df_company_group = df_company_group.groupby(['company_group'], as_index=False).agg(
        {'payment_amount': 'sum'})



    df_company_group.sort_values(by="payment_amount", inplace=True)
    payment_amount_list = list(df_company_group['payment_amount'])
    company_group_list = list(df_company_group['company_group'])
    payment_amount_max_value = max(payment_amount_list) * 1.02
    payment_amount_min_value = min(payment_amount_list) - min(payment_amount_list) * 0.3


    fig = go.Figure(go.Bar(
        x=payment_amount_list,
        y=company_group_list,
        text=payment_amount_list,
        marker={"color": '#32935F'},
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
        texttemplate='%{text:.2s}',
        # texttemplate='%{x}%',
        hovertemplate='%{y}: %{x}'
    )



    output_div = dcc.Graph(config={'displayModeBar': False}, figure=fig)
    # print(df_company_group)

    # output_div='test'

    return output_div
