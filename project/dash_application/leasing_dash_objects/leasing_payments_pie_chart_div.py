from dash import dcc, html
import plotly.graph_objects as go
import plotly.express as px
import datetime
import dash_application.dash_objects.initial_values as initial_values
from dash import dash_table
import pandas as pd
def leasing_payments_pie_chart_div_func(leasing_payment_graph_df, agreement_status_select):
    full_agreement_status_select = list(leasing_payment_graph_df['current_agreement_status'].unique())
    agreement_status_filter = full_agreement_status_select
    if agreement_status_select:
        if 'list' in (str(type(agreement_status_select))):
            agreement_status_filter = agreement_status_select
        else:
            agreement_status_filter = []
            agreement_status_filter.append(agreement_status_select)

    df = leasing_payment_graph_df.loc[
        leasing_payment_graph_df['current_agreement_status'].isin(agreement_status_filter)]

    # определяем жирность категорий
    df_categories = df.groupby(['current_agreement_status'], as_index=False).agg({'payment_amount': 'sum'})
    df_categories.sort_values(by="payment_amount", ascending=False, inplace=True)
    # df_categories["cumpercentage"] = df_categories["payment_amount"].cumsum() / df_categories['payment_amount'].sum() * 100
    df_categories["share"] = df_categories["payment_amount"] / df_categories['payment_amount'].sum() * 100
    df_categories_magor = df_categories.loc[df_categories['share']>=1]
    df_categories_minor = df_categories.loc[df_categories['share'] < 1]

    df_categories_minor_total_sum = df_categories_minor['payment_amount'].sum()
    if df_categories_minor_total_sum >0:
        added_other_df = pd.DataFrame([{'current_agreement_status':'Другое', 'payment_amount': df_categories_minor_total_sum}])
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
        values.append(value)
        colors.append(colors_dict[i])
        i=i+1

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
        # texttemplate='%{value} млрд.руб',
        # hovertemplate='%{y}: %{text} млрд.руб'

    )

    # temp_df['payment_amount'] = temp_df['payment_amount'].round(decimals =3)
    leasing_payments_piechart_graph = dcc.Graph(
        figure=fig,
        config={'displayModeBar': False},
        style={"height": "100%", "width": "100%"}
    )
    return [leasing_payments_piechart_graph]