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


def taken_vs_remain_v3_func(data_input, transhi_i_crediti_block_creditor_select, credit_line_type_select):
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
            # query = 'SELECT *  FROM "creditDB";'
            query = 'SELECT *  FROM "creditdb_2";'
            df_credit_main = pd.read_sql(query, con)
        # df_credit_main.rename(columns={
        #     'sum': 'amount'
        # }, inplace=True)

        with engine.connect() as con:
            # query = 'SELECT *  FROM "creditDB";'
            query_creditnewdata = 'SELECT *  FROM "creditnewdata";'
            try:
                df_creditnewdata = pd.read_sql(query_creditnewdata, con)
            except Exception as e:
                output_object_list.append(f'df_creditnewdata: {e}')

        df_credit_main = pd.concat([df_credit_main, df_creditnewdata])

        ########################## ПРИМЕНЕНИЕ ФИЛЬТРОВ ######################################################
        df_credit_main['credit_line_type'] = df_credit_main['credit_line_type'].replace('', 'Не возобновляемая')
        full_credit_line_types = ['Возобновляемая', 'Не возобновляемая']
        credit_line_type_list = full_credit_line_types
        if credit_line_type_select:
            if 'list' in str(type(credit_line_type_select)):
                credit_line_type_list = credit_line_type_select
            else:
                credit_line_type_list = []
                credit_line_type_list.append(credit_line_type_select)

        df_credit_main = df_credit_main.loc[df_credit_main['credit_line_type'].isin(credit_line_type_list)]

        # Получаем полный список банков, если в селекте кредиторов пусто
        full_creditor_list = list(df_credit_main['creditor'].unique())
        full_creditor_list_df_creditnewdata = list(df_creditnewdata['creditor'].unique())
        full_creditor_list_ = full_creditor_list + full_creditor_list_df_creditnewdata
        updated_full_creditor_list = []
        for creditor in full_creditor_list_:
            if creditor not in updated_full_creditor_list:
                updated_full_creditor_list.append(creditor)

        full_creditor_list = updated_full_creditor_list

        creditor_list = full_creditor_list
        if transhi_i_crediti_block_creditor_select:
            if 'list' in str(type(transhi_i_crediti_block_creditor_select)):
                creditor_list = transhi_i_crediti_block_creditor_select
            else:
                creditor_list = []
                creditor_list.append(transhi_i_crediti_block_creditor_select)




        df_credit_main = df_credit_main.loc[df_credit_main['creditor'].isin(creditor_list)]


        # df_creditnewdata = df_creditnewdata.loc[df_creditnewdata['credit_line_type'].isin(credit_line_type_list)]


        # df_creditnewdata = df_creditnewdata.loc[df_creditnewdata['creditor'].isin(creditor_list)]

        ########################## КОНЕЦ ПРИМЕНЕНИЯ ФИЛЬТРОВ ######################################################

        df_credit_main['date'] = pd.to_datetime(df_credit_main['date'])
        ######################## заполняем пустые ячейки ########################

        df_credit_main['agreement_code'].fillna('Кредиты', inplace=True)
        df_credit_main['agreement_code'] = df_credit_main['agreement_code'].replace(r'', 'Кредиты', regex=True)

        df_credit_main['credit_volume'].fillna(0, inplace=True)
        df_credit_main['credit_volume'] = df_credit_main['credit_volume'].replace('', 0, regex=True)

        df_credit_main['amount'].fillna(0, inplace=True)
        df_credit_main['amount'] = df_credit_main['amount'].replace('', 0, regex=True)

        df_credit_main['credit_tranch_date'].fillna(datetime.datetime(2050,1,1), inplace=True)
        df_credit_main['credit_tranch_date'] = df_credit_main['credit_tranch_date'].replace('', datetime.datetime(2050,1,1), regex=True)

        # Прописываем дату начала контракта
        df_credit_main = df_credit_main.loc[df_credit_main['agreement_code'] == 'Кредиты']
        # получаем список договоров
        agreement_list = list(df_credit_main['contract_title'].unique())

        for agreement in agreement_list:
            agreement_df = df_credit_main.loc[df_credit_main['contract_title']==agreement]
            contract_title_text = agreement_df.iloc[0]['contract_title']
            # получаем первую запись, когда по договору был первый транш.
            agreement_df = agreement_df.copy()
            agreement_df.sort_values(['credit_tranch_date'], inplace=True, ignore_index=True)
            try:
                credit_agreement_first_date = agreement_df.iloc[0, agreement_df.columns.get_loc("credit_tranch_date")]
            except:
                credit_agreement_first_date = datetime.datetime(datetime.datetime.now().year, 1,1).date()

                # получаем дату начала действия договора, извлекая ее из текста
            try:
                date_record = re.search("[0-9]{1,2}.[0-9]{1,2}.[0-9]{4}",
                                        contract_title_text).group()
                credit_agreement_first_date = datetime.datetime.strptime(date_record, '%d.%m.%Y')
            except Exception as e:
                # date_record_temp.append(e)
                pass
            credit_agreement_first_date = credit_agreement_first_date.date()
            """type: date"""
            df_credit_main.loc[df_credit_main['contract_title']==agreement, ['credit_agreement_first_date']] = credit_agreement_first_date



        #################################################################################################
        #################################################################################################
        df_credit_main.sort_values(['credit_tranch_date'], inplace=True, ignore_index=True)
        transh_first_date = df_credit_main.iloc[0, df_credit_main.columns.get_loc("credit_agreement_first_date")]

        # # год даты первого транша:
        transh_first_date_year = transh_first_date.year
        # 1 января года первого транша
        transh_first_date_year_first_date = datetime.datetime(transh_first_date_year, 1, 1)

        current_year = datetime.datetime.now().year
        current_year_first_date = datetime.datetime(current_year, 1, 1)
        current_year_last_date = datetime.datetime(current_year+1, 1, 1)


        df_result_list = []
        temp_date = transh_first_date_year_first_date
        while temp_date <= current_year_last_date:
            temp_dict = {}
            temp_dict['datetime'] = temp_date
            temp_dict['date'] = temp_date.date()
            temp_dict['allowance'] = 0
            temp_dict['allowance_cumulative'] = 0
            temp_dict['credit_tranch'] = 0
            temp_dict['tranch_cumulative'] = 0
            temp_dict['credit_payments'] = 0
            temp_dict['payments_cumulative'] = 0
            temp_dict['credit_limit'] = 0
            temp_dict['credit_limit_updated_current_year'] = 0

            df_result_list.append(temp_dict)
            temp_date = temp_date + datetime.timedelta(days=1)

        df_tranch_data = pd.DataFrame(df_result_list)
        #
        # df_credit_limit_data = pd.DataFrame(df_result_list)
        # итерируемся по договорам для включения ограничений по срокам лимитов
        agreement_list = list(df_credit_main['contract_title'].unique())

        date_allowance_df = pd.DataFrame()
        date_tranches_df = pd.DataFrame()
        merge_table = pd.DataFrame()
        merge_table_2 = pd.DataFrame()
        df_tranch_data_ = pd.DataFrame()
        for contract_name in agreement_list:

            ######################################## credit tranches ##########################################
            ###################################################################################################
            # Получаем данные по траншам кредитов
            df_credit_main_ = df_credit_main.loc[df_credit_main['credit_tranch_date'] != datetime.datetime(2050, 1, 1)]

            contract_df = df_credit_main_.loc[df_credit_main_['contract_title'] == str(contract_name)]
            date_tranches_df = contract_df.groupby(['credit_tranch_date'], as_index=False).agg({'credit_volume': 'max'})
            date_tranches_df['credit_tranch_date_date'] = pd.to_datetime(date_tranches_df['credit_tranch_date']).dt.date

            df_tranch_data_ = df_tranch_data.merge(date_tranches_df, left_on='date',
                                                   right_on='credit_tranch_date_date', how='left')

            df_tranch_data_['credit_volume'].fillna(0, inplace=True)
            df_tranch_data_['credit_volume'] = df_tranch_data_['credit_volume'].replace('', 0)
            df_tranch_data_['credit_tranch'] = df_tranch_data_['credit_tranch'] + df_tranch_data_['credit_volume']
            df_tranch_data_['credit_tranch_cumulative_cumsum'] = df_tranch_data_['credit_tranch'].cumsum()
            df_tranch_data_['tranch_cumulative'] = df_tranch_data_['tranch_cumulative'] + df_tranch_data_['credit_tranch_cumulative_cumsum']

            df_tranch_data = df_tranch_data_.loc[:, ['date', 'allowance', 'allowance_cumulative', 'credit_tranch', 'tranch_cumulative', 'credit_payments', 'payments_cumulative', 'credit_limit', 'credit_limit_updated_current_year']]

            ######################################## credit payments ##########################################
            ###################################################################################################
            contract_df = df_credit_main.loc[df_credit_main['contract_title'] == str(contract_name)]
            payments_filtered_df = contract_df.loc[contract_df['credit_line_type'] == 'Возобновляемая']
            date_payments_df = payments_filtered_df.groupby(['date'], as_index=False).agg({'amount': 'sum'})
            date_payments_df['date_date'] = pd.to_datetime(date_payments_df['date']).dt.date

            df_tranch_data_payments = df_tranch_data.merge(date_payments_df, left_on='date', right_on='date_date', how='left')
            df_tranch_data_payments['amount'].fillna(0, inplace=True)
            df_tranch_data_payments['amount'] = df_tranch_data_payments['amount'].replace('', 0)
            df_tranch_data_payments['credit_payments'] = df_tranch_data_payments['credit_payments'] + df_tranch_data_payments['amount']
            df_tranch_data_payments.rename(columns={
                    'date_x': 'date'
                    }, inplace=True)


            df_tranch_data_payments['credit_payments_cumulative'] = df_tranch_data_payments['credit_payments'].cumsum()
            df_tranch_data_payments['payments_cumulative'] = df_tranch_data_payments['payments_cumulative'] + df_tranch_data_payments['credit_payments_cumulative']

            df_tranch_data = df_tranch_data_payments.loc[:,
                             ['date', 'allowance', 'allowance_cumulative', 'credit_tranch', 'tranch_cumulative',
                              'credit_payments', 'payments_cumulative', 'credit_limit',
                              'credit_limit_updated_current_year']]



            ##################################### allowance ########################################
            ########################################################################################
            contract_df = df_credit_main.loc[df_credit_main['contract_title'] == str(contract_name)]
            contract_df = contract_df.copy()
            contract_df.sort_values(['credit_tranch_date'], inplace=True, ignore_index=True)

            date_allowance_df = contract_df.groupby(
                ['contract_title', 'credit_line_type', 'limitdeadline', 'ral_credit_transh_getting_deadline',
                 'credit_agreement_first_date'],
                as_index=False).agg({'credit_agreement_total_volume': 'max'})

            df_tranch_data_ = df_tranch_data.merge(date_allowance_df, left_on='date',
                                                   right_on='credit_agreement_first_date', how='left')

            df_tranch_data_['credit_agreement_total_volume'].fillna(0, inplace=True)
            df_tranch_data_['credit_agreement_total_volume'] = df_tranch_data_['credit_agreement_total_volume'].replace(
                '', 0)

            df_tranch_data_['allowance'] = df_tranch_data_['allowance'] + df_tranch_data_[
                'credit_agreement_total_volume']
            df_tranch_data_['allowance_cumulative_cumsum'] = df_tranch_data_['allowance'].cumsum()

            # значение накопленной на сегодняшний день суммы выплат по кредиту
            df_payments_till_today = df_tranch_data_.loc[df_tranch_data_['date'] <= datetime.datetime.now().date()]
            payment_till_today_value = df_payments_till_today['payments_cumulative'].max()

            df_tranch_data_.loc[df_tranch_data_['date'] > datetime.datetime.now().date(), [
                'payments_before_today']] = payment_till_today_value

            df_tranch_data_['credit_limit_agreement'] = df_tranch_data_['allowance_cumulative_cumsum'] + \
                                                        df_tranch_data_['payments_before_today']

            df_tranch_data_['allowance_cumulative'] = df_tranch_data_['allowance_cumulative'] + df_tranch_data_[
                'credit_limit_agreement']



            ################################### ЗДЕСЬ НАДО ОБРЕЗАТЬ КРЕДИТНЫЙ ЛИМИТ В ДОГОВОРЕ ################
            ral_credit_transh_getting_deadline = contract_df.iloc[0]['ral_credit_transh_getting_deadline']
            """type: datetime"""
            ral_credit_transh_getting_deadline_date = ral_credit_transh_getting_deadline.date()
            """type: date"""

            limitdeadline = contract_df.iloc[0]['limitdeadline']
            """type: datetime"""
            limitdeadline_date = limitdeadline.date()
            """type: date"""

            # ral_credit_transh_getting_deadline = datetime.datetime(2023,2,1)
            # limitdeadline_date = datetime.datetime(2023, 3, 27).date()

            credit_limit_df_min_date = df_tranch_data_payments['date'].min()
            credit_limit_df_max_date = df_tranch_data_payments['date'].max()

            if ral_credit_transh_getting_deadline_date >= credit_limit_df_min_date and ral_credit_transh_getting_deadline_date <= credit_limit_df_max_date:
                if ral_credit_transh_getting_deadline_date < limitdeadline_date:
                    # рассчитываем сумму задолжености как разницу значения tranch_cumulative и payments_cumulative
                    ral_credit_transh_getting_deadline_tranch_cumulative_value_df = df_tranch_data_.loc[df_tranch_data_['date'] == ral_credit_transh_getting_deadline_date]
                    ral_credit_transh_getting_deadline_tranch_cumulative_value = ral_credit_transh_getting_deadline_tranch_cumulative_value_df.iloc[0]['tranch_cumulative']
                    ral_credit_transh_getting_deadline_payments_cumulative_value = ral_credit_transh_getting_deadline_tranch_cumulative_value_df.iloc[0]['payments_cumulative']

                    dolg_amount = ral_credit_transh_getting_deadline_tranch_cumulative_value - ral_credit_transh_getting_deadline_payments_cumulative_value
                    df_tranch_data_.loc[df_tranch_data_['date'] > ral_credit_transh_getting_deadline_date, ['credit_limit_agreement']] = dolg_amount


            # обнуление значений после даты limitdeadline_date
            df_tranch_data_.loc[df_tranch_data_['date'] > limitdeadline_date, ['credit_limit_agreement']] = 0

            ################################## КОНЕЦ ОБРЕЗАНИЯ КРЕДИТНОГО ЛИМИТА В ДОГОВОРЕ################################################################
            df_tranch_data = df_tranch_data_.loc[:,
                             ['date', 'allowance', 'allowance_cumulative', 'credit_tranch', 'tranch_cumulative',
                              'credit_payments', 'payments_cumulative', 'credit_limit',
                              'credit_limit_updated_current_year']]


        ######################################### ПОСТРОЕНИЕ ГРАФИКА #########################################

        df_tranch_data_graph = df_tranch_data.loc[df_tranch_data['date']>=datetime.datetime(current_year, 1, 1).date()]
        # значение траншей в точке 1 января 2023 года
        current_year_transh_value_df = df_tranch_data.loc[df_tranch_data['date']==datetime.datetime(current_year, 1,1).date(), ['tranch_cumulative']]
        current_year_transh_value = current_year_transh_value_df.iloc[0]['tranch_cumulative']
        # output_object_list.append(current_year_transh_value)
        df_tranch_data_graph['tranch_cumulative_current_year'] = df_tranch_data_graph['tranch_cumulative'] - current_year_transh_value

        df_tranch_data_by_year_till_today = df_tranch_data_graph.loc[df_tranch_data_graph['date'] <= datetime.datetime.now().date()]

        df_tranch_data_graph['credit_limit_current_year'] = df_tranch_data_graph['credit_limit'] - current_year_transh_value
        # df_tranch_data_graph['credit_limit_current_year_module'] = df_tranch_data_graph['credit_limit_current_year']
        # df_tranch_data_graph.loc[df_tranch_data_graph['credit_limit_current_year']<0 , ['credit_limit_current_year_module']] = 0

        # отрицательные  точки в ряду credit_limit_current_year надо сделать нулем
        df_tranch_data_graph.loc[df_tranch_data_graph['credit_limit_current_year']<0] = 0


        # округляем
        # y_tranch_raw_list = list(df_tranch_data_by_year_till_today['tranch_cumulative']/1000000000)
        y_tranch_raw_list = list(df_tranch_data_by_year_till_today['tranch_cumulative_current_year'] / 1000000000)
        y_tranch_rounded_value_list = []
        for x in y_tranch_raw_list:
            x_rounded = rd(x, 3)
            y_tranch_rounded_value_list.append(x_rounded)

        # y_remains_raw_list = list(df_tranch_data_graph['credit_limit']/1000000000)
        y_remains_raw_list = list(df_tranch_data_graph['credit_limit_current_year'] / 1000000000)
        y_remains_rounded_value_list = []
        for x in y_remains_raw_list:
            x_rounded = rd(x, 3)
            y_remains_rounded_value_list.append(x_rounded)

        fig = go.Figure()
        x_tranch = df_tranch_data_by_year_till_today['date']
        y_tranch = y_tranch_rounded_value_list


        x_remains = df_tranch_data_graph['date']
        y_remains = y_remains_rounded_value_list

        fig.add_trace(go.Scatter(x=x_tranch, y=y_tranch, name='Транши', fill='tozeroy', line={'color': '#FFC000'}))
        fig.add_trace(go.Scatter(x=x_remains, y=y_remains, name='Лимиты',
                                 # fill='tonexty'
                                 ))

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

        data = df_tranch_data.to_dict('records')
        credit_datatable = dash_table.DataTable(data=data, )

        taken_vs_remain_v2_func_check_ = html.Div(
            children=[

                str(date_record_temp),
                html.Div(
                    children=output_object_list
                ),
                # datatable_df_tranch_data_,
                credit_datatable
            ]
        )

        output = fig_div
        return output, taken_vs_remain_v2_func_check_










                    # contract_df_dolg['date'] = pd.to_datetime(contract_df_dolg['date'])
                    # contract_df_dolg_future = contract_df_dolg.loc[contract_df_dolg['date']>datetime.datetime(2023,2,1)]
            #             contract_df_dolg_future['date_date'] = contract_df_dolg_future['date'].dt.date
            #             contract_df_dolg_future = contract_df_dolg_future.loc[:, ['date_date', 'amount']]
            #             total_dolg_amount = contract_df_dolg_future['amount'].sum()
            #
            #
            #             # теперь надо этим диктом заменить данные в credit_limit_df
            #             # credit_limit_df.loc[credit_limit_df['date']>=ral_credit_transh_getting_deadline_date, ['credit_limit_with_deadline']] = total_dolg_amount
            #             # limitdeadline_date
            #             # try:
            #             #     credit_limit_df['credit_limit_with_deadline'] = credit_limit_df.apply(
            #             #         lambda x: x['credit_limit'] if (x['date'] <= ral_credit_transh_getting_deadline_date) else total_dolg_amount, axis=1)
            #             # except Exception as e:
            #             #     output_object_list.append(f'стрельнуло здесь 1')
            #             try:
            #                 credit_limit_df['credit_limit'] = credit_limit_df.apply(
            #                     lambda x: x['credit_limit'] if (x['date'] <= ral_credit_transh_getting_deadline_date) else total_dolg_amount, axis=1)
            #             except Exception as e:
            #                 output_object_list.append(f'стрельнуло здесь 1')
            #
            #
            #
            #     #################################################################################











            # получаем таблицу date - tranches
            ############## исключаем строки с 2050 годом в credit_tranch_date потому что они не нужны для траншей ########
            # df_credit_main_ = df_credit_main.loc[df_credit_main['credit_tranch_date'] != datetime.datetime(2050, 1, 1)]
            #
            # date_tranches_df = df_credit_main_.groupby(['credit_tranch_date'],
            #                                           as_index=False).agg({'credit_volume': 'max'})
            #
            # date_tranches_df['credit_tranch_date_date'] = pd.to_datetime(date_tranches_df['credit_tranch_date']).dt.date
            #
            # merge_table_2 = merge_table.merge(date_tranches_df, left_on='date', right_on='credit_tranch_date_date',
            #                                   how='left')
            #
            # merge_table_2['credit_volume'].fillna(0, inplace=True)
            # merge_table_2['credit_volume'] = merge_table_2['credit_volume'].replace('', 0)
            # merge_table_2['credit_volume_cumulative'] = merge_table_2['credit_volume'].cumsum()
            # merge_table_2 = merge_table_2.loc[:,
            #                 ['date', 'credit_agreement_total_volume', 'contract_allowance_cumulative', 'credit_volume',
            #                  'credit_volume_cumulative']]

        #     # получаем таблицу date - payments
        #     date_payments_filtered_df = df_credit_main.loc[df_credit_main['credit_line_type'] == 'Возобновляемая']
        #
        #     date_payments_df = date_payments_filtered_df.groupby(['date'],
        #                                                          as_index=False).agg({'amount': 'sum'})
        #
        #
        #
        #     date_payments_df['date_date'] = pd.to_datetime(date_payments_df['date']).dt.date
        #
        #     date_payments_df['payment_until_today'] = date_payments_df.apply(
        #         lambda x: x['amount'] if (x['date_date'] <= datetime.datetime.now().date()) else 0, axis=1)
        #
        #
        #     merge_table_3 = merge_table_2.merge(date_payments_df, left_on='date', right_on='date_date',
        #                                         how='left')
        #     merge_table_3['payment_until_today'].fillna(0, inplace=True)
        #     merge_table_3['payment_until_today'] = merge_table_3['payment_until_today'].replace('', 0)
        #     merge_table_3['amount_cumulative'] = merge_table_3['payment_until_today'].cumsum()
        #
        #     merge_table_3.rename(columns={
        #         'date_x': 'date'
        #     }, inplace=True)
        #
        #     credit_limit_df = merge_table_3.loc[:,
        #                       ['date', 'credit_agreement_total_volume', 'contract_allowance_cumulative',
        #                        'credit_volume', 'credit_volume_cumulative', 'amount', 'amount_cumulative']]
        #
        #     credit_limit_df['credit_limit'] = credit_limit_df['contract_allowance_cumulative'] - credit_limit_df[
        #         'credit_volume_cumulative'] + credit_limit_df['amount_cumulative']
        #
        #     limitdeadline = contract_df.iloc[0]['limitdeadline']
        #     limitdeadline_date = limitdeadline.date()
        #     credit_limit_df_min_date = credit_limit_df['date'].min()
        #     credit_limit_df_max_date = credit_limit_df['date'].max()
        #
        #     # limitdeadline_date = datetime.datetime(2023, 3, 27).date()
        #
        #     #################################### Здесь  - ограничения по датам Срока получения траншей ###############
        #
        #     ral_credit_transh_getting_deadline = contract_df.iloc[0]['limitdeadline']
        #     """type: datetime"""
        #
        #     ral_credit_transh_getting_deadline_date = ral_credit_transh_getting_deadline.date()
        #
        #     # определяем объем задолженности
        #     contract_df_dolg = contract_df.groupby(['date'],as_index=False).agg({'amount': 'sum'})
        #
        #     # ral_credit_transh_getting_deadline_date = datetime.datetime(2023,2,1).date()
        #
        #     if ral_credit_transh_getting_deadline_date >= credit_limit_df_min_date and ral_credit_transh_getting_deadline_date <= credit_limit_df_max_date:
        #
        #         if ral_credit_transh_getting_deadline_date < limitdeadline_date:
        #             contract_df_dolg['date'] = pd.to_datetime(contract_df_dolg['date'])
        #             contract_df_dolg_future = contract_df_dolg.loc[contract_df_dolg['date']>datetime.datetime(2023,2,1)]
        #             contract_df_dolg_future['date_date'] = contract_df_dolg_future['date'].dt.date
        #             contract_df_dolg_future = contract_df_dolg_future.loc[:, ['date_date', 'amount']]
        #             total_dolg_amount = contract_df_dolg_future['amount'].sum()
        #
        #
        #             # теперь надо этим диктом заменить данные в credit_limit_df
        #             # credit_limit_df.loc[credit_limit_df['date']>=ral_credit_transh_getting_deadline_date, ['credit_limit_with_deadline']] = total_dolg_amount
        #             # limitdeadline_date
        #             # try:
        #             #     credit_limit_df['credit_limit_with_deadline'] = credit_limit_df.apply(
        #             #         lambda x: x['credit_limit'] if (x['date'] <= ral_credit_transh_getting_deadline_date) else total_dolg_amount, axis=1)
        #             # except Exception as e:
        #             #     output_object_list.append(f'стрельнуло здесь 1')
        #             try:
        #                 credit_limit_df['credit_limit'] = credit_limit_df.apply(
        #                     lambda x: x['credit_limit'] if (x['date'] <= ral_credit_transh_getting_deadline_date) else total_dolg_amount, axis=1)
        #             except Exception as e:
        #                 output_object_list.append(f'стрельнуло здесь 1')
        #
        #
        #
        #     #################################################################################
        #
        #     ########## доработаем текущую credit_limit_df
        #     # credit_limit_df['credit_limit_'] = credit_limit_df['credit_limit']
        #     #################################### Здесь  - ограничения по датам срока действия лимита ###############
        #
        #
        #     if limitdeadline_date >= credit_limit_df_min_date and limitdeadline_date <= credit_limit_df_max_date:
        #         # try:
        #         #     credit_limit_df['credit_limit_with_deadline'] = credit_limit_df.apply(
        #         #         lambda x: x['credit_limit_with_deadline'] if (x['date'] <= limitdeadline_date) else 0, axis=1)
        #         # except Exception as e:
        #         #     output_object_list.append(f'стрельнуло здесь 2')
        #         try:
        #             credit_limit_df['credit_limit'] = credit_limit_df.apply(
        #                 lambda x: x['credit_limit'] if (x['date'] <= limitdeadline_date) else 0, axis=1)
        #         except Exception as e:
        #             output_object_list.append(f'стрельнуло здесь 2')
        #     ###########################  КОНЕЦ ограничения по датам срока действия лимита  ######################################################
        #
        #     # data__ = credit_limit_df.to_dict('records')
        #     # credit_datatable = dash_table.DataTable(data=data__, )
        #     # # output_object_list.append(str(contract_df_dolg_future_dict))
        #     # output_object_list.append(credit_datatable)
        #
        #
        #
        #     # credit_limit_df_ = credit_limit_df.loc[:, ['date', 'credit_limit_with_deadline']]
        #     credit_limit_df_ = credit_limit_df.loc[:, ['date', 'credit_limit']]
        #
        #
        #     df_credit_limit_data = df_credit_limit_data.merge(credit_limit_df_, on='date', how='left')
        #
        #
        #     # df_credit_limit_data['credit_limit_total'] =df_credit_limit_data['credit_limit_total'] + df_credit_limit_data['credit_limit_with_deadline']
        #     df_credit_limit_data['credit_limit_total'] = df_credit_limit_data['credit_limit_total'] + df_credit_limit_data['credit_limit']
        #
        #
        #     df_credit_limit_data = df_credit_limit_data.loc[:, ['date', 'credit_limit_total']]


        # data_date_tranches_df = df_tranch_data_payments.to_dict('records')
        # datatable_df_tranch_data_ = dash_table.DataTable(data=data_date_tranches_df, )


