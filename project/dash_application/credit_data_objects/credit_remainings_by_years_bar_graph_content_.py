import datetime
from dash import html, dcc
import plotly.graph_objects as go
import pandas as pd

def credit_remainings_by_years_bar_graph_content_func(df, bank, creditor_select, credit_contract_select, credit_year_select, credit_tab_quarter_select, credit_tab_month_select):
    output = 'credit_treemap_div_content'
    df['year'] = df['year'].astype(float)
    df['year'] = df['year'].astype('int')
    # режем df по фильтрам

    # фильтр по кредитору ###########################################################################
    creditor_full_list = list(df['creditor'].unique())
    creditor_filter = creditor_full_list
    if creditor_select:
        if 'list' in str(type(creditor_select)):
            creditor_filter = creditor_select
        else:
            creditor_filter = list(creditor_select)

    # режем выборку по кредитору
    df = df.loc[df['creditor'].isin(creditor_filter)]

    #####################################################################################################

    # фильтр по credit_contract ##########################################################################
    credit_contract_full_list = list(df['credit_contract'].unique())
    credit_contract_filter = credit_contract_full_list
    if credit_contract_select:
        if 'list' in str(type(credit_contract_select)):
            credit_contract_filter = credit_contract_select
        else:
            credit_contract_filter = list(credit_contract_select)

    # режем выборку по credit_contract
    df = df.loc[df['credit_contract'].isin(credit_contract_filter)]
    #####################################################################################################

    # фильтр по годам ###########################################################################
    year_full_list = list(df['year'].unique())
    year_filter = year_full_list
    if credit_year_select:
        if 'list' in str(type(credit_year_select)):
            year_filter = credit_year_select
        else:
            year_filter = [credit_year_select]

    year_filter_int_list = []
    for year in year_filter:
        year = int(year)
        if year >= int(datetime.datetime.now().year):
            year_filter_int_list.append(year)

    # режем выборку по годам
    df = df.loc[df['year'].isin(year_filter_int_list)]
    #####################################################################################################

    # фильтр по кварталам ###########################################################################
    quarter_full_list = list(df['quarter'].unique())
    quarter_filter = quarter_full_list
    if credit_tab_quarter_select:
        if 'list' in str(type(credit_tab_quarter_select)):
            quarter_filter = credit_tab_quarter_select
        else:
            quarter_filter = [credit_tab_quarter_select]

    quarter_filter_int_list = []
    for quarter in quarter_filter:
        quarter = int(quarter)
        quarter_filter_int_list.append(quarter)

    # режем выборку по кварталам
    df = df.loc[df['quarter'].isin(quarter_filter_int_list)]
    #####################################################################################################

    # фильтр по месяцам ###########################################################################
    month_full_list = [1,2,3,4,5,6,7,8,9,10,11,12]
    month_filter = month_full_list
    if credit_tab_month_select:
        if 'list' in str(type(credit_tab_month_select)):
            month_filter = credit_tab_month_select
        else:
            month_filter = [credit_tab_month_select]

    month_filter_int_list = []
    for month in month_filter:
        month = int(month)
        month_filter_int_list.append(month)

    df['date_2'] = pd.to_datetime(df['date'])
    if "int" in str(df['date'].dtype):
        df['date_2'] = pd.to_datetime(df['date'], unit='ms')
    df['month'] = df['date_2'].dt.month
    # режем выборку по месяцам
    df = df.loc[df['month'].isin(month_filter_int_list)]
    #####################################################################################################



    today = datetime.datetime.now()

    try:
        df = df.loc[df['date'] >= today]
    except:
        df = df.loc[df['date'] >= today.date()]


    # режем по кликнутому банку
    df = df.loc[df['creditor']==bank]

    df = df.loc[df['agreement_code'] == "Кредиты"]
    df_groupped = df.groupby(['year'], as_index=False).agg(
        {'amount': 'sum'})
    df_groupped.sort_values(by="year", inplace=True)

    df_groupped['year'] = df_groupped['year'].astype('str')

    fig = go.Figure(go.Bar(
        x=df_groupped['year'],
        y=df_groupped['amount'] / 1000000000,
        text=df_groupped['amount'] / 1000000000,
        marker=dict(color="#FFC000")
    ))

    fig.update_layout({
        'margin': dict(l=5, r=5, t=45, b=5),
        "bargap": 0.30,
        # 'barmode': 'stack',
        "title": f"Погашение кредитного портфеля {bank}",
        # 'legend': {
        #     'orientation': "h",
        #     'yanchor': "bottom",
        #     'y': 1.08,
        # }
    })
    fig.update_xaxes(
        # dtick="M1",
        # tickformat="%y",
        # rangeslider_visible=True
    )
    fig.update_traces(
        texttemplate='%{text:.3f} млрд.руб',
        hovertemplate='<extra></extra>%{x}:<br>%{text:.3f} млрд.руб',
    )
    return fig


