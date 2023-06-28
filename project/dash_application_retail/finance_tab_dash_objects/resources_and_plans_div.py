import os
from sqlalchemy import create_engine
import pandas as pd
import datetime
from dash import dash_table
from dash import html
import re
import plotly.graph_objects as go
from dash import dcc
import time
import dash_application_retail.colors as colors_file
from scipy import stats
import random
def rd(x, y=3):
    ''' A classical mathematical rounding by Voznica '''
    m = int('1' + '0' * y)  # multiplier - how many positions to the right
    q = x * m  # shift to the right by multiplier
    c = int(q)  # new number
    i = int((q - c) * 10)  # indicator number on the right
    if i >= 5:
        c += 1
    return c / m


def resources_and_plans_div_func(finance_tab_top_client_filter):
    output = ''
    taken_vs_remain_v2_func_check_ = ""
    date_record_temp = []
    credit_datatable = ""
    # credit_limit_df = pd.DataFrame()
    output_object_list = []
    resources_today = ''


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
    if finance_tab_top_client_filter:
        if 'list' in str(type(finance_tab_top_client_filter)):
            creditor_list = finance_tab_top_client_filter
        else:
            creditor_list = []
            creditor_list.append(finance_tab_top_client_filter)




    df_credit_main = df_credit_main.loc[df_credit_main['creditor'].isin(creditor_list)]


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

    # меняем дату на оси х на таймстамп
    x_transhes_updated = []
    for date_item in x_transhes:
        time_st = time.mktime(date_item.timetuple())
        x_transhes_updated.append(time_st)

    slope, intercept, r, p, std_err = stats.linregress(x_transhes_updated, y_transhes)
    def myfunc(x):
        return slope * x + intercept

    x_full_axis = []
    for date_item in x_limit:
        time_st = time.mktime(date_item.timetuple())
        x_full_axis.append(time_st)


    mymodel = list(map(myfunc, x_full_axis))

    # ищем точку пересечения mymodel с линией тренда
    # итерируемся по mymodel и ищем есть ли пересечение
    index_y_limit = 0
    mymodel_max_date = max(x_limit)

    distances_list = []


    for mymodel_item in mymodel:
        # получаем индекс в листе mymodel
        current_mymodel_index = mymodel.index(mymodel_item)

        # получаем значение по этому индексу в листе y_limit
        current_y_limit_value = y_limit[current_mymodel_index]

        # получаем расстояние от лимита до тренда
        distance = current_y_limit_value - mymodel_item



        # записываем полученное значение в список
        distances_list.append(distance)

    # определяем есть ли пересечение знака
    element_sign = 'origin'
    if distances_list[0]<0:
        for item in distances_list:
            if item >=0:
                element_sign = 'changed'
    elif distances_list[0]>0:
        for item in distances_list:
            if item <=0:
                element_sign = 'changed'

    abs_distance_list = []
    date_min_distance = max(x_limit)

    x_trend = x_limit
    y_trend = mymodel
    max_y_trend_value = max(mymodel)
    if element_sign == 'changed': # находим меньшее по модулю число

        for item in distances_list:
            item_abs = abs(item)
            abs_distance_list.append(item_abs)

        min_abs_distance_value = min(abs_distance_list)
        min_abs_distance_index = abs_distance_list.index(min_abs_distance_value)
        # получаем значение по иксу в котором найдено минимальное значение дистанции
        x_limit = list(x_limit)
        date_min_distance = x_limit[min_abs_distance_index]

        # обрезаем ряды по эту дату
        x_trend = x_limit[0:min_abs_distance_index+1]
        y_trend = mymodel[0:min_abs_distance_index+1]

        max_y_trend_value = max(y_trend)




    x_remaining = graph_df['date']
    # y_remaining = graph_df['free_remaining']
    y_remaining =  free_remaining_current_year_list

    first_main_color = colors_file.colors_dict[0]
    second_main_color = colors_file.colors_dict[1]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_limit, y=y_limit, name='План', line={'color': first_main_color}
                             # fill='tonexty'
                             ))
    fig.add_trace(go.Scatter(x=x_transhes, y=y_transhes, name='Ресурсы', fill='tozeroy', line={'color': second_main_color}))

    fig.add_trace(go.Scatter(x=x_remaining, y=y_remaining, name='Остаток', line={'color': 'green'}, opacity=0, showlegend=False), )

    # fig.add_trace(go.Scatter(x=x_trend, y=y_trend, line={'color': 'red'}, name='Тренд'))

    # добавляем пунктирную линию если тренд пересек лимит
    y_trace_to_limit_trend = []
    x_trace_to_limit_trend = []
    if element_sign == 'changed':

        for y_limit_item in y_trend:
            if y_limit_item > max_y_trend_value:
                break
            item = y_limit_item
            if item>=0:
                y_trace_to_limit_trend.append(item)

        number_of_elements_in_y_trace_to_limit_trend = len(y_trace_to_limit_trend)
        for i in range(number_of_elements_in_y_trace_to_limit_trend):
            x_trace_to_limit_trend.append(date_min_distance)

        # fig.add_trace(go.Scatter(x=x_trace_to_limit_trend, y=y_trace_to_limit_trend, line={'color': 'grey', 'dash': 'dot'}, showlegend=False))

        x_trace_to_limit_trend_update = x_trend + x_trace_to_limit_trend
        y_trace_to_limit_trend_update = y_trend + y_trace_to_limit_trend
        fig.add_trace(go.Scatter(x=x_trace_to_limit_trend_update, y=y_trace_to_limit_trend_update, line={'color': 'red', 'dash': 'dot'}, name='Тренд'))


    fig.add_vline(
        x=datetime.datetime.now(),
        # line_width=3,
        # line_dash="dash",
        line_color="lightgrey")

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

    # data = graph_df.to_dict('records')
    # credit_datatable = dash_table.DataTable(data=data, )
    # credit_datatable = ""


    # получаем значение остатка в сегодняшний день
    graph_df_today_df = graph_df.loc[graph_df['date']==datetime.datetime.now().date()]
    free_remaining_value = graph_df_today_df.iloc[0]['free_remaining']
    free_remaining = free_remaining_value
    free_remaining = str(x_trace_to_limit_trend)

    # Получаем значение ресурсов (выручки в сегодняшний день)
    resources_today = y_transhes[-1]
    random.seed(3)
    random_ebitda_value = resources_today * random.uniform(0.13, 0.28)

    ebitda = random_ebitda_value
    ebitda_str = '{:.3f}'.format(ebitda)

    random.seed(3)
    profit = random_ebitda_value / resources_today * 100
    profit_str = '{:.1f}%'.format(profit)

    # profit_str = f'resources_today: {resources_today}, ebitda: {ebitda}, profit: {profit} ebitda_str: {ebitda_str}'
    # profit_str = f'{ebitda_str}'
    return [
        output,
        taken_vs_remain_v2_func_check_,
        free_remaining,
        resources_today,
        ebitda_str,
        profit_str
    ]