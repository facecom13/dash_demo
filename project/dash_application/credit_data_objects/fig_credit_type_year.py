import datetime
from dash import html, dcc
import plotly.graph_objects as go
import pandas as pd

def fig_credit_type_year_func(df, creditor_select, credit_contract_select, credit_year_select, credit_tab_quarter_select, credit_tab_month_select):

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

    df.sort_values(by="date", inplace=True)
    # df['year'] = df['year_dt'].dt.year
    df_groupped = df.groupby(['year', 'agreement_code'], as_index=False).agg(
        {'amount': 'sum'})

    df_totals = df.groupby(['year'], as_index=False).agg({'amount': 'sum'})
    df_totals['amount'] = df_totals['amount'] / 1000000000
    df_totals['amount'] = df_totals['amount'].round(decimals=3)
    df_totals['total_label'] = df_totals['amount'] * 1

    labels = list(df_totals['amount'])
    labels_total = list(df_totals['total_label'])
    year_x = list(df_totals['year'])

    fig_credit_type = go.Figure()
    # получаем список видов
    credit_type_select_list = list(df_groupped['agreement_code'].unique())
    colors = ["#FFC000", "#32935F"]
    i = 0

    for credit_type in credit_type_select_list:
        temp_credit_df = df_groupped.loc[df_groupped['agreement_code'] == credit_type]
        temp_credit_df = temp_credit_df.copy()
        # temp_credit_df['year'] = temp_credit_df['year_dt'].dt.year
        temp_credit_df = temp_credit_df.copy()
        temp_credit_df['amount'] = temp_credit_df['amount'] / 1000000000
        temp_credit_df['amount'] = temp_credit_df['amount'].round(decimals=3)

        x_credit = list(temp_credit_df['year'])
        y_credit = list(temp_credit_df['amount'])
        fig_credit_type.add_trace(go.Bar(
            x=x_credit,
            y=y_credit,
            name=credit_type,
            # text = y_credit,
            marker=dict(color=colors[i])
        ))
        i = i + 1
    fig_credit_type.add_trace(go.Scatter(
        x=year_x,
        y=labels_total,
        text=labels,
        mode='text',
        textposition='top center',
        textfont=dict(
            size=18,
        ),
        showlegend=False
    ))
    fig_credit_type.update_layout({
        'barmode': 'stack',
        'margin': dict(l=5, r=5, t=5, b=5),
        # "title": "Погашение кредитного портфеля",
        'legend': {
            'orientation': "h",
            'yanchor': "bottom",
            'y': 1.08,
        }
    })
    fig_credit_type.update_xaxes(
        # dtick="%Y",
        # tickformat="%Y",
        # rangeslider_visible=True
        type='category'
    )
    fig_credit_type.update_traces(
        # texttemplate='%{text:.3f} млрд.руб',
        hovertemplate='<extra></extra>%{x}:<br>%{y:.3f} млрд.руб',
    )

    return fig_credit_type