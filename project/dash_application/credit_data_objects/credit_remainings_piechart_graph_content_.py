import datetime
from dash import html, dcc
import plotly.graph_objects as go
import pandas as pd

def credit_remainings_piechart_graph_content_func(df, creditor_select, credit_contract_select, credit_year_select, credit_tab_quarter_select, credit_tab_month_select):
    output = 'credit_treemap_div_content'
    output_div = "no data"
    first_date = ''
    last_date = ''
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

    if len(df)>0:

        credit_banks_df = df.loc[df['agreement_code'] == 'Кредиты']
        fig = go.Figure()
        # Если данных в df нет, то отдаем сообщение, что данных нет
        # if len(credit_banks_df) == 0:
        #     fig.update_xaxes(
        #         {'visible': False}
        #     )
        #     fig.update_yaxes(
        #         {'visible': False}
        #     )
        #     fig.add_annotation(
        #         # x=2, y=5,
        #         text="Нет данных для построения графика",
        #         showarrow=False,
        #         # xref = "paper",
        #         # yref =  "paper",
        #
        #     )
        #     return fig

        credit_bank_list = list(credit_banks_df['creditor'].unique())

        # Получаем список значений с суммами кредитов
        bank_credit_value_list = []
        df_graph_list = []
        for bank in credit_bank_list:
            temp_dict = {}
            bank_filtered_df = credit_banks_df.loc[credit_banks_df['creditor'] == bank]
            total_bank_credit_value = bank_filtered_df['amount'].sum()
            temp_dict['bank'] = bank
            temp_dict['amount'] = total_bank_credit_value
            bank_credit_value_list.append(total_bank_credit_value)
            df_graph_list.append(temp_dict)
        df_graph = pd.DataFrame(df_graph_list)
        df_graph['amount'] = df_graph['amount'] / 1000000000
        df_graph['amount'] = df_graph['amount'].round(decimals=3)
        df_graph.sort_values(by=['amount'], ascending=True, inplace=True)

        labels = df_graph['bank']
        values = df_graph['amount']
        colors = ['#B99B6B', '#698269', '#183A1D', '#F0A04B', '#E1EEDD', "#b27aa1", "#E8E8E8", "#b3e5ca", "#FFC000",
                  "#E8E8E8", "#909090", "#32935F"]
        colors = ["#b27aa1", "#E8E8E8", "#b3e5ca", "#FFC000", "#E8E8E8", "#909090", "#32935F"]
        # colors_dict = initial_values.colors_dict
        #
        # myKeys = list(colors_dict.keys())
        # myKeys.sort(reverse=False)
        # sorted_dict = {i: colors_dict[i] for i in myKeys}
        #
        # colors = list(sorted_dict.values())
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            textinfo='label+percent'
        )])
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.2,
            xanchor="right",
            x=1
        ))
        fig.update_traces(
            marker=dict(colors=colors),
            textposition='auto',
            # texttemplate='%{value} млрд.руб',
            # hovertemplate='%{y}: %{text} млрд.руб'

        )

        # получаем первую дату в выборке
        df.sort_values(['date'], inplace=True)
        first_date = df.iloc[0, df.columns.get_loc("date")]
        first_date = today
        last_date = df.iloc[-1, df.columns.get_loc("date")]

        output_div = dcc.Graph(figure=fig,config={'displayModeBar': False})

    return output_div, first_date, last_date