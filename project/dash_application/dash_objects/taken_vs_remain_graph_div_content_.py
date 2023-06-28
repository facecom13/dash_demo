import plotly.graph_objects as go
from dash import dcc
import datetime
import pandas as pd

def taken_vs_remain_graph_div_content_func(df, transhi_i_crediti_block_creditor_select):
    fig = go.Figure()
    year_in_filter = int(datetime.datetime.now().year)
    # Получаем полный список банков, если в селекте кредиторов пусто
    full_creditor_list = list(df['creditor'].unique())
    creditor_list = full_creditor_list
    if transhi_i_crediti_block_creditor_select:
        if 'list' in str(type(transhi_i_crediti_block_creditor_select)):
            creditor_list = transhi_i_crediti_block_creditor_select
        else:
            creditor_list = []
            creditor_list.append(transhi_i_crediti_block_creditor_select)
    # if taken_vs_remain_year_select:
    #     year_in_filter = int(taken_vs_remain_year_select)


    first_day_of_year_selection = datetime.datetime(year_in_filter, 1, 1)
    last_day_of_year_selection = datetime.datetime(year_in_filter + 1, 1, 1)
    today = datetime.datetime.now()
    current_year = today.year
    # определяем последний день в выборке
    last_date_of_selection = today
    if year_in_filter != current_year:
        last_date_of_selection = last_day_of_year_selection

    # получаем первую дату транша
    df.sort_values(['credit_tranch_date'], inplace=True, ignore_index=True)
    transh_first_date = df.iloc[0, df.columns.get_loc("credit_tranch_date")]

    # год даты первого транша:
    transh_first_date_year = transh_first_date.year
    # 1 января года первого транша
    transh_first_date_year_first_date = datetime.datetime(transh_first_date_year, 1, 1)

    # 1 января года за текущим
    current_year_last_date = datetime.datetime(current_year+1, 1, 1)

    # cоздаем массив из ежедневных дат от начала выплаты траншей до конца текущего года
    df_result_list = []
    temp_date = transh_first_date_year_first_date
    while temp_date <= current_year_last_date:
        temp_dict = {}
        temp_dict['datetime'] = temp_date
        temp_dict['date'] = temp_date.date()
        temp_dict['creditor'] = ""
        temp_dict['tranch_volume'] = 0
        temp_dict['total_credit_volume'] = 0
        temp_dict['credit_limit'] = 0
        temp_dict['payment']=0

        df_result_list.append(temp_dict)
        temp_date = temp_date + datetime.timedelta(days=1)

    df_tranch_data = pd.DataFrame(df_result_list)
    df_tranch_data.sort_values(['date'], inplace=True)
    df_tranch_data['year'] = df_tranch_data['datetime'].dt.year

    # режем выборку по кредиторам
    df_filtered = df.loc[df['creditor'].isin(creditor_list)]



    # надо заполнить df_tranch_data  - в соответствующую дату вставить значение выплаты по кредиту
    # при этом надо заполнить creditor, date, amount
    # temp_df - это отфильтрованная по contract_name выборка
    df_filtered_2 = df_filtered.loc[df_filtered['agreement_code'] == 'Кредиты']
    for row in df_filtered_2.itertuples():
        creditor = getattr(row, 'creditor')
        payment = getattr(row, 'amount')
        payment_datetime = getattr(row, 'date')
        payment_date = payment_datetime.date()

        # текущее значение в payment в df_tranch_data:
        current_payment_value_df_row = df_tranch_data.loc[df_tranch_data['date']==payment_date]['payment']
        # прибавляем текущее к payment
        updated_payment_value = current_payment_value_df_row + payment

        # переписываем значение payment в df_tranch_data
        df_tranch_data.loc[df_tranch_data['date'] == payment_date, ['payment']] = updated_payment_value
        df_tranch_data.loc[df_tranch_data['date'] == payment_date, ['creditor']] = creditor
    ####### здесь df_tranch_data должна быть заполнена данными о кредитных выплатах
    # создаем колонку с кумулятивным payment
    df_tranch_data['payment_until_today'] = df_tranch_data.apply(lambda x: x['payment'] if (x['datetime'] <= datetime.datetime.now()) else 0, axis=1)
    # df_tranch_data['payment_cumulative'] = df_tranch_data['payment'].cumsum()
    df_tranch_data['payment_cumulative'] = df_tranch_data['payment_until_today'].cumsum()



    # получаем список договоров
    agreement_list = list(df_filtered['contract_title'].unique())
    # получаем стоимость всех кредитов, вошедших в выборку
    total_credits_volume = 0
    df_filtered = df_filtered.copy()
    df_filtered['tranch_id'] = df_filtered['credit_tranch_date'].astype(str)+"_" + df_filtered['contract_title']

    for contract_name in agreement_list:
        temp_df = df_filtered.loc[df_filtered['contract_title'] == contract_name]
        credit_volume_by_contract = temp_df.iloc[0, temp_df.columns.get_loc("credit_agreement_total_volume")]
        temp_df = temp_df.copy()
        temp_df.sort_values(['credit_tranch_date'], inplace=True, ignore_index=True)

        # получаем первую запись, когда по договору был первый транш. Будем считать это активацией договора
        credit_agreement_activation_date = temp_df.iloc[0, df.columns.get_loc("credit_tranch_date")]
        credit_agreement_credit_limit = temp_df.iloc[0, df.columns.get_loc("credit_agreement_total_volume")]
        # Обновляем данные в df_tranch_data
        current_credit_limit_value = df_tranch_data.loc[df_tranch_data['date'] == credit_agreement_activation_date.date(), ['credit_limit']]
        updated_credit_limit_value = current_credit_limit_value + credit_agreement_credit_limit
        df_tranch_data.loc[df_tranch_data['date'] == credit_agreement_activation_date.date(), ['credit_limit']] = updated_credit_limit_value




        # получаем список траншей в выборке по договору
        tranch_list_in_contract = list(temp_df['tranch_id'].unique())
        # внутри выборки по договору итерируемся по траншам
        for tranch in tranch_list_in_contract:
            temp_tranch_df = temp_df.loc[temp_df['tranch_id']==tranch]
            # дата транша
            tranch_date  = temp_tranch_df.iloc[0, temp_tranch_df.columns.get_loc("credit_tranch_date")]
            tranch_id_ = tranch
            creditor = temp_tranch_df.iloc[0, temp_tranch_df.columns.get_loc("creditor")]
            tranch_volume = temp_tranch_df.iloc[0, temp_tranch_df.columns.get_loc("credit_amount")]
            total_credit_volume = temp_tranch_df.iloc[0, temp_tranch_df.columns.get_loc("credit_agreement_total_volume")]

            # Обновляем данные в df_tranch_data
            current_tranch_volume_value =  df_tranch_data.loc[df_tranch_data['date']==tranch_date.date(), ['tranch_volume']]
            updated_tranch_volume_value = current_tranch_volume_value + tranch_volume
            df_tranch_data.loc[df_tranch_data['date']==tranch_date.date(), ['tranch_volume']] = updated_tranch_volume_value
            df_tranch_data.loc[df_tranch_data['date'] == tranch_date.date(), ['total_credit_volume']] = total_credit_volume
            df_tranch_data.loc[df_tranch_data['date'] == tranch_date.date(), ['creditor']] = creditor

    # получаем колонку с накопительным итогом траншей
    df_tranch_data['tranch_cumulative'] = df_tranch_data['tranch_volume'].cumsum()
    # Получаем колонку с накопительным итогом кредитных лимитов
    df_tranch_data['credit_limit_cumulative'] = df_tranch_data['credit_limit'].cumsum()
    df_tranch_data['credit_limit_cumulative_with_payments'] = df_tranch_data['credit_limit_cumulative'] + df_tranch_data['payment_cumulative']


    ####### Для каждого дня свободный остаток - это разница между кредитным лимитом и суммой траншей
    df_tranch_data['remains_cumultive'] = df_tranch_data['credit_limit_cumulative_with_payments'] - df_tranch_data['tranch_cumulative']
    # print(df_tranch_data)
    # print(df_tranch_data.loc[df_tranch_data['credit_limit']!=0])
    x_tranch = df_tranch_data['date']
    y_tranch = df_tranch_data['tranch_cumulative']
    x_remains = df_tranch_data['date']
    y_remains = df_tranch_data['credit_limit_cumulative']

    # режем выборку по годам
    # year_filter_list = list(df['credit_tranch_date'].dt.year.unique())
    # if taken_vs_remain_year_select:
    #     if 'list' in str(type(taken_vs_remain_year_select)):
    #         year_filter_list = []
    #         for i in taken_vs_remain_year_select:
    #             year_filter_list.append(int(i))
    #     else:
    #         year_filter_list = []
    #         year_filter_list.append(int(taken_vs_remain_year_select))
    year_filter_list = [year_in_filter]
    df_tranch_data_by_year = df_tranch_data.loc[df_tranch_data['year'].isin(year_filter_list)]

    # определяем значение в первом дне в получившейся выборке
    first_date_transh_value = df_tranch_data_by_year.iloc[0, df_tranch_data_by_year.columns.get_loc("tranch_cumulative")]
    # значение транша в этот день

    # вычитаем это значение из всех точек
    df_tranch_data_by_year = df_tranch_data_by_year.copy()
    df_tranch_data_by_year['tranch_cumulative_year'] = df_tranch_data_by_year['tranch_cumulative']-first_date_transh_value
    df_tranch_data_by_year['credit_limit_cumulative_year'] = df_tranch_data_by_year['credit_limit_cumulative_with_payments']-first_date_transh_value

    # обрезаем выборку до сегодняшнего дня
    df_tranch_data_by_year_till_today = df_tranch_data_by_year.loc[df_tranch_data_by_year['date'] <=today.date()]

    df_tranch_data_by_year_till_today  = df_tranch_data_by_year_till_today.copy()
    df_tranch_data_by_year_till_today['tranch_cumulative_year'] = df_tranch_data_by_year_till_today['tranch_cumulative_year'] / 1000000000
    df_tranch_data_by_year_till_today['tranch_cumulative_year'] = df_tranch_data_by_year_till_today['tranch_cumulative_year'].round(decimals=3)

    df_tranch_data_by_year = df_tranch_data_by_year.copy()
    df_tranch_data_by_year['credit_limit_cumulative_year'] = df_tranch_data_by_year['credit_limit_cumulative_year'] / 1000000000
    df_tranch_data_by_year['credit_limit_cumulative_year'] = df_tranch_data_by_year['credit_limit_cumulative_year'].round(decimals=3)

    x_tranch = df_tranch_data_by_year_till_today['date']
    y_tranch = df_tranch_data_by_year_till_today['tranch_cumulative_year']
    x_remains = df_tranch_data_by_year['date']
    y_remains = df_tranch_data_by_year['credit_limit_cumulative_year']


    fig.add_trace(go.Scatter(x=x_tranch, y=y_tranch, name= 'Транши', fill='tozeroy', line={'color':'#FFC000'}))  # fill down to xaxis
    fig.add_trace(go.Scatter(x=x_remains, y=y_remains, name='Лимиты',
                             # fill='tonexty'
                             ))  # fill to trace0 y
    # print("taken_vs_remain_year_select:", taken_vs_remain_year_select)
    today_txt = today.strftime("%d.%m.%Y")
    # сегодняшнее значение суммы выданных траншей
    df_tranch_data_by_year_today_df = df_tranch_data.loc[df_tranch_data['date']==today.date()]
    # значение выданных траншей на 1 января
    df_tranch_data_by_start2023_df = df_tranch_data.loc[df_tranch_data['date'] == datetime.datetime(2023,1,1).date()]

    today_tranch_value = df_tranch_data_by_year_today_df.iloc[0, df_tranch_data_by_year_today_df.columns.get_loc("tranch_cumulative")]

    beginning_of_2023_tranch_value =  df_tranch_data_by_start2023_df.iloc[0, df_tranch_data_by_start2023_df.columns.get_loc("tranch_cumulative")]
    tranch_volume_from_beginning_of_2023 = today_tranch_value - beginning_of_2023_tranch_value


    # сегодняшнее значение суммы кредитных лимитов
    today_credit_limit = df_tranch_data_by_year_today_df.iloc[0, df_tranch_data_by_year_today_df.columns.get_loc("credit_limit_cumulative")]

    # сегодняшнее значение свободного остатка
    today_free_remains = today_credit_limit - today_tranch_value

    today_tranch_value_txt = str(round(tranch_volume_from_beginning_of_2023/1000000000, 3)) + " млрд"
    today_free_remains = str(round(today_free_remains/1000000000, 3)) + " млрд"

    # annotation_text = f"На {today_txt}:<br>Выбрано: {today_tranch_value_txt} <br>Свободный остаток: {today_free_remains}"
    #
    # fig.add_annotation(
    #     x=0.3,
    #     y=1.2,
    #     text=annotation_text,
    #     align="left",
    #     showarrow=False,
    #     xref = "paper",
    #     yref =  "paper",
    #     # bordercolor="#c7c7c7",
    #     # borderwidth=2,
    #     # borderpad=4,
    #     bgcolor="white",
    #     opacity=0.8
    # )


    # if int(taken_vs_remain_year_select) == 2023:

    fig.add_vline(
        x=today,
        # line_width=3,
        # line_dash="dash",
        line_color="#32935F")
    fig.update_layout(
        # title='Транши и лимиты',
        margin= dict(l=5, r=5, t=75, b=5),
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


    fig_div = dcc.Graph(figure=fig, config = {'displayModeBar': False})

    return fig_div