import os
from sqlalchemy import create_engine
import pandas as pd
import datetime
from dash import dash_table
from dash import html
import re
import plotly.graph_objects as go
from dash import dcc
def rd(x, y=3):
    ''' A classical mathematical rounding by Voznica '''
    m = int('1' + '0' * y)  # multiplier - how many positions to the right
    q = x * m  # shift to the right by multiplier
    c = int(q)  # new number
    i = int((q - c) * 10)  # indicator number on the right
    if i >= 5:
        c += 1
    return c / m


def taken_vs_remain_v5_func(data_input, transhi_i_crediti_block_creditor_select, credit_line_type_select):
    output = ''
    taken_vs_remain_v2_func_check_ = ""
    date_record_temp = []
    credit_datatable = ""
    # credit_limit_df = pd.DataFrame()
    output_object_list = []

    if data_input == '1с_api':
        url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
        engine = create_engine(url_db, pool_recycle=3600)
        with engine.connect() as con:
            query = 'SELECT *  FROM "transhes_and_limits";'
            df_credit_main = pd.read_sql(query, con)
        # df_credit_main.rename(columns={
        #     'sum': 'amount'
        # }, inplace=True)



        ########################## ПРИМЕНЕНИЕ ФИЛЬТРОВ ######################################################

        # Получаем полный список банков, если в селекте кредиторов пусто
        full_creditor_list = list(df_credit_main['creditor'].unique())

        creditor_list = full_creditor_list
        if transhi_i_crediti_block_creditor_select:
            if 'list' in str(type(transhi_i_crediti_block_creditor_select)):
                creditor_list = transhi_i_crediti_block_creditor_select
            else:
                creditor_list = []
                creditor_list.append(transhi_i_crediti_block_creditor_select)




        df_credit_main = df_credit_main.loc[df_credit_main['creditor'].isin(creditor_list)]

        full_credit_line_type = ['Возобновляемая', 'Не возобновляемая']

        credit_line_type_list = full_credit_line_type
        if credit_line_type_select:
            if 'list' in str(type(credit_line_type_select)):
                credit_line_type_list = credit_line_type_select
            else:
                credit_line_type_list = []
                credit_line_type_list.append(credit_line_type_select)

        df_credit_main = df_credit_main.loc[df_credit_main['credit_line_type'].isin(credit_line_type_list)]


        ########################## КОНЕЦ ПРИМЕНЕНИЯ ФИЛЬТРОВ ######################################################




        graph_df = df_credit_main.groupby(['date', 'datetime'],as_index=False).agg({'credit_limit': 'sum', 'transh_cumsum': 'sum', 'free_remaining':'sum'})
        # graph_df.sort_values(['date'], inplace=True)
        # значение траншей 1 января 2023
        graph_df['date_str'] =  graph_df['date'].astype(str)
        graph_df['datetime'] = pd.to_datetime(graph_df['datetime'])
        graph_df = graph_df.loc[graph_df['datetime']>=datetime.datetime(2023,1,1)]
        graph_df = graph_df.loc[graph_df['datetime'] < datetime.datetime(2024, 1, 1)]

        min_date = graph_df['datetime'].min()

        transh_value_at_year_start = 0
        try:
            transh_value_at_year_start_df = graph_df.loc[graph_df['date_str'] == '2023-01-01']
            transh_value_at_year_start = transh_value_at_year_start_df.iloc[0]['transh_cumsum']
        except:
            pass

        # if min_date<datetime.datetime(2023,1,1):
        #     transh_value_at_year_start_df = graph_df.loc[graph_df['date_str']=='2023-01-01']
        #     transh_value_at_year_start = transh_value_at_year_start_df.iloc[0]['transh_cumsum']
        # else:
        #     transh_value_at_year_start = 0




        graph_df['credit_limit_current_year'] = graph_df['credit_limit'] - transh_value_at_year_start

        # нули убираем, если они есть
        graph_df['credit_limit_updated'] = graph_df['credit_limit_current_year']
        graph_df.loc[graph_df['credit_limit_current_year']<=0, ['credit_limit_updated']] = 0


        graph_df['transh_current_year'] = graph_df['transh_cumsum'] - transh_value_at_year_start
        graph_df.loc[graph_df['transh_current_year'] <= 0, ['transh_current_year_updated']] = 0


        transh_data_df = graph_df.loc[graph_df['datetime']<=datetime.datetime.now()]

        graph_df['credit_limit_updated'] = graph_df['credit_limit_updated']/1000000000
        credit_limit_current_year_list = []
        temp_list = list(graph_df['credit_limit_updated'])
        for item in temp_list:
            credit_limit_current_year_rounded = rd(item, 3)
            credit_limit_current_year_list.append(credit_limit_current_year_rounded)

        transh_data_df['transh_current_year'] = transh_data_df['transh_current_year'] / 1000000000
        transh_current_year_list = []
        temp_list = list(transh_data_df['transh_current_year'])
        for item in temp_list:
            transh_current_year_rounded = rd(item, 3)
            transh_current_year_list.append(transh_current_year_rounded)

        graph_df['free_remaining'] = graph_df['free_remaining'] / 1000000000
        free_remaining_current_year_list = []
        temp_list = list(graph_df['free_remaining'])
        for item in temp_list:
            free_remaining_current_year_rounded = rd(item, 3)
            free_remaining_current_year_list.append(free_remaining_current_year_rounded)


        x_limit = graph_df['date']
        # y_limit = graph_df['credit_limit_current_year']
        y_limit = credit_limit_current_year_list

        x_transhes = transh_data_df['date']
        # y_transhes = transh_data_df['transh_current_year']
        y_transhes =transh_current_year_list

        x_remaining = graph_df['date']
        # y_remaining = graph_df['free_remaining']
        y_remaining =  free_remaining_current_year_list

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_limit, y=y_limit, name='Лимиты',
                                 # fill='tonexty'
                                 ))
        fig.add_trace(go.Scatter(x=x_transhes, y=y_transhes, name='Транши', fill='tozeroy', line={'color': '#FFC000'}))

        fig.add_trace(go.Scatter(x=x_remaining, y=y_remaining, name='Остаток', line={'color': 'green'}, opacity=0))

        fig.add_vline(
            x=datetime.datetime.now(),
            # line_width=3,
            # line_dash="dash",
            line_color="#32935F")

        fig.update_layout(
            # title='Транши и лимиты',
            margin=dict(l=5, r=5, t=75, b=5),
        )
        fig.update_layout(
            {
                'legend': {
                    'orientation': "h",
                    'yanchor': "bottom",
                    'y': 1.08,
                }
            }
        )
        fig.update_traces(
            mode="lines",
            # hovertemplate=None
        )
        fig.update_layout(hovermode="x unified")

        fig_div = dcc.Graph(figure=fig, config={'displayModeBar': False})
        output = fig_div

        data = graph_df.to_dict('records')
        credit_datatable = dash_table.DataTable(data=data, )
        # credit_datatable = ""
        taken_vs_remain_v2_func_check_ = credit_datatable

        # получаем значение остатка в сегодняшний день
        graph_df_today_df = graph_df.loc[graph_df['date']==datetime.datetime.now().date()]
        free_remaining_value = graph_df_today_df.iloc[0]['free_remaining']
        free_remaining = free_remaining_value

        return output, taken_vs_remain_v2_func_check_, free_remaining