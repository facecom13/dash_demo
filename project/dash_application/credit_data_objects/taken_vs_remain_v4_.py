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


def taken_vs_remain_v4_func(data_input, transhi_i_crediti_block_creditor_select, credit_line_type_select):
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
            credit_agreement_first_datetime = credit_agreement_first_date
            credit_agreement_first_date = credit_agreement_first_date.date()
            """type: date"""
            df_credit_main.loc[df_credit_main['contract_title']==agreement, ['credit_agreement_first_date']] = credit_agreement_first_date
            df_credit_main.loc[df_credit_main['contract_title'] == agreement, ['credit_agreement_first_datetime']] = credit_agreement_first_datetime


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
        payment_last_date = df_credit_main['date'].max()


        df_result_list = []
        temp_date = transh_first_date_year_first_date
        while temp_date <= current_year_last_date:
            temp_dict = {}
            temp_dict['datetime'] = temp_date
            temp_dict['date'] = temp_date.date()
            # temp_dict['contract_name'] = ""
            #
            # temp_dict['allowance'] = 0
            # temp_dict['allowance_cumulative'] = 0
            # temp_dict['credit_limit_cumulative'] = 0
            # temp_dict['credit_tranch'] = 0
            # temp_dict['tranch_cumulative'] = 0
            # temp_dict['credit_payments'] = 0
            # temp_dict['payments_cumulative'] = 0
            # temp_dict['payments_cumulative_before_today'] = 0
            # temp_dict['payments_cumulative_after_today'] = 0
            # temp_dict['payments_flat_after_today'] = 0

            # temp_dict['credit_limit'] = 0

            df_result_list.append(temp_dict)
            temp_date = temp_date + datetime.timedelta(days=1)

        df_tranch_data = pd.DataFrame(df_result_list)

        agreement_list = list(df_credit_main['contract_title'].unique())
        payments_total_df = pd.DataFrame()

        ######################################## credit payments ##########################################
        ###################################################################################################
        for contract_name in agreement_list:

            contract_df = df_credit_main.loc[df_credit_main['contract_title'] == str(contract_name)]

            payments_df = contract_df.groupby(['date','agreement_code', 'creditor', 'contract_title', 'credit_line_type'], as_index=False).agg({'amount': 'sum'})

            payments_df['date_date'] = pd.to_datetime(payments_df['date']).dt.date
            # payments_df_merged = df_tranch_data.merge(payments_df, left_on='date', right_on='date_date',
            #                                                how='left')
            payments_total_df = pd.concat([payments_total_df, payments_df])

        payments_total_df.sort_values(['date'], inplace=True, ignore_index=True)

        ######################################## credit tranches ##########################################
        ###################################################################################################
        transhes_total_df = pd.DataFrame()
        transhes_df_trach_id = pd.DataFrame()
        transhes_df = pd.DataFrame()
        tranch_list = list(df_credit_main['transh_id'].unique())

        tranch_result_list=[]

        for transh_id in tranch_list:
            temp_dict = {}
            tranche_data_df = df_credit_main.loc[df_credit_main['transh_id'] == str(transh_id)]
            # tranche_data_df = tranche_data_df.reset_index(drop=True)
            tranch_volume = tranche_data_df['credit_volume'].max()
            transh_date = tranche_data_df['credit_tranch_date'].max()
            temp_dict['transh_id'] = transh_id
            temp_dict['transh_date'] = transh_date
            temp_dict['tranch_volume'] = tranch_volume

            tranch_result_list.append(temp_dict)


        transh_df = pd.DataFrame(tranch_result_list)


        ######################################## credit limits ##########################################
        ###################################################################################################
        agreement_list = list(df_credit_main['contract_title'].unique())
        credit_limit_result_list = []
        for agreement in agreement_list:
            temp_dict = {}
            agreement_df = df_credit_main.loc[df_credit_main['contract_title'] == agreement]
            creditor = agreement_df.iloc[0]['creditor']
            credit_agreement_total_volume =agreement_df.iloc[0]['credit_agreement_total_volume']
            limitdeadline = agreement_df.iloc[0]['limitdeadline']
            ral_credit_transh_getting_deadline = agreement_df.iloc[0]['ral_credit_transh_getting_deadline']
            credit_agreement_first_date = agreement_df.iloc[0]['credit_agreement_first_date']

            temp_dict['creditor'] = creditor
            temp_dict['agreement'] = agreement
            temp_dict['credit_agreement_total_volume'] = credit_agreement_total_volume
            temp_dict['limitdeadline'] = limitdeadline
            temp_dict['ral_credit_transh_getting_deadline'] = ral_credit_transh_getting_deadline
            temp_dict['credit_agreement_first_date'] = credit_agreement_first_date
            credit_limit_result_list.append(temp_dict)

        credit_limit_df = pd.DataFrame(credit_limit_result_list)

        # data_temp = credit_limit_df.to_dict('records')
        # datatable_temp = dash_table.DataTable(data=data_temp, )
        # output_object_list.append(creditor)
        # output_object_list.append(credit_agreement_total_volume)
        # output_object_list.append(limitdeadline)
        # output_object_list.append(datatable_temp)

        #################################################################################
        #################################################################################
        #################################################################################
        # собираем

        # Получаем таблицу payments и мерджим ее с df_tranch_data
        payments_total_df_restored = payments_total_df.loc[payments_total_df['credit_line_type'] == 'Возобновляемая']
        payments_df = payments_total_df_restored.groupby(['date'], as_index=False).agg({'amount': 'sum'})
        payments_df['date_date'] = payments_df['date'].dt.date
        payments_df_tranch_data = df_tranch_data.merge(payments_df, left_on='date', right_on='date_date', how='left')

        payments_df_tranch_data.rename(columns={
                    'date_x': 'date'
                }, inplace=True)
        payments_df_tranch_data['amount'].fillna(0, inplace=True)
        payments_df_tranch_data['amount'] = payments_df_tranch_data['amount'].replace('', 0)
        payments_df_tranch_data['payments_cumulative'] = payments_df_tranch_data['amount'].cumsum()
        payments_df_tranch_data = payments_df_tranch_data.loc[:, ['date', 'amount', 'payments_cumulative']]

        #################################################################################
        #################################################################################
        # Получаем таблицу tranch и мерджим ее с payments_df_tranch_data
        tranches_df = transh_df.groupby(['transh_date'], as_index=False).agg({'tranch_volume': 'sum'})
        tranches_df['date_date'] = tranches_df['transh_date'].dt.date
        tranches_df_tranch_data = payments_df_tranch_data.merge(tranches_df, left_on='date', right_on='date_date', how='left')
        tranches_df_tranch_data.rename(columns={
            'date_x': 'date'
        }, inplace=True)
        tranches_df_tranch_data['tranch_volume'].fillna(0, inplace=True)
        tranches_df_tranch_data['tranch_volume'] = tranches_df_tranch_data['tranch_volume'].replace('', 0)
        tranches_df_tranch_data['tranch_cumulative'] = tranches_df_tranch_data['tranch_volume'].cumsum()
        tranches_df_tranch_data = tranches_df_tranch_data.loc[:, ['date', 'amount', 'payments_cumulative', 'tranch_volume', 'tranch_cumulative']]

        #################################################################################
        #################################################################################
        # Получаем таблицу credit limit и мерджим ее с tranches_df_tranch_data
        credit_limit_df = credit_limit_df.groupby(['credit_agreement_first_date', 'limitdeadline','agreement', 'ral_credit_transh_getting_deadline'], as_index=False).agg({'credit_agreement_total_volume': 'sum'})
        # credit_limit_df['date_date'] = credit_limit_df['credit_agreement_first_date'].dt.date
        limits_df_tranch_data = tranches_df_tranch_data.merge(credit_limit_df, left_on='date', right_on='credit_agreement_first_date', how='left')
        limits_df_tranch_data.rename(columns={
            'date_x': 'date'
        }, inplace=True)
        limits_df_tranch_data['credit_agreement_total_volume'].fillna(0, inplace=True)
        limits_df_tranch_data['credit_agreement_total_volume'] = limits_df_tranch_data['credit_agreement_total_volume'].replace('', 0)
        limits_df_tranch_data['credit_limit_cumulative'] = limits_df_tranch_data['credit_agreement_total_volume'].cumsum()
        limits_df_tranch_data = limits_df_tranch_data.loc[:,['date', 'amount', 'payments_cumulative', 'tranch_volume', 'tranch_cumulative','agreement', 'credit_agreement_total_volume', 'limitdeadline', 'ral_credit_transh_getting_deadline', 'credit_limit_cumulative']]

        #################################################################################
        #################################################################################
        # Получаем таблицу задолженности по договору


        # Получаем первую дату начала действия договора во всем массиве. Это будет начало таблицы с датами

        credit_agreement_first_datetime = df_credit_main['credit_agreement_first_datetime'].min()
        # output_object_list.append(f'credit_agreement_first_datetime: {credit_agreement_first_datetime}')

        # получаем дату последнего платежа во всем массиве
        df_credit_credit_payments = df_credit_main.loc[df_credit_main['date']!=datetime.datetime(2050,1,1)]
        last_payment_datetime = df_credit_credit_payments['date'].max()
        # output_object_list.append(f'last_payment_date_date: {last_payment_datetime}')




        df_result_list = []
        temp_date = pd.to_datetime(credit_agreement_first_datetime)
        last_payment_datetime = pd.to_datetime(last_payment_datetime)
        while temp_date <= last_payment_datetime:
            temp_dict = {}
            temp_dict['datetime'] = temp_date
            temp_dict['date'] = temp_date.date()
            temp_dict['credit_allowance'] = 0

            df_result_list.append(temp_dict)
            temp_date = temp_date + datetime.timedelta(days=1)

        df_calendar_data = pd.DataFrame(df_result_list)
        temp_df = pd.DataFrame()
        contract_df = pd.DataFrame()

        credit_limit_data_df = pd.DataFrame()
        for contract_name in agreement_list:
            contract_df = df_credit_main.loc[df_credit_main['contract_title'] == str(contract_name)]
            contract_df = contract_df.copy()
            contract_df['date_time'] = pd.to_datetime(contract_df['date'])

            contract_credit_agreement_first_date = datetime.datetime(2050,1,1).date()
            contract_credit_agreement_first_datetime = datetime.datetime(2050, 1, 1).date()
            try:
                contract_credit_agreement_first_date = contract_df['credit_agreement_first_date'].min()
                contract_credit_agreement_first_datetime = contract_df['credit_agreement_first_datetime'].min()
                # output_object_list.append(f'contract_credit_agreement_first_date: {contract_credit_agreement_first_date}')
            except Exception as e:
                output_object_list.append(f'ошибка при получении contract_credit_agreement_first_date: {e}')

            contract_credit_allowance = 0
            try:
                contract_credit_allowance = contract_df['credit_agreement_total_volume'].max()
                # output_object_list.append(f'contract_credit_allowance: {contract_credit_allowance}')
            except Exception as e:
                output_object_list.append(f'ошибка при получении contract_credit_allowance: {e}')

            data_calendar_credit_allowance_current_value_df = df_calendar_data.loc[df_calendar_data['date']==contract_credit_agreement_first_date, ['credit_allowance']]
            data_calendar_credit_allowance_current_value_ = data_calendar_credit_allowance_current_value_df.iloc[0]['credit_allowance']
            # output_object_list.append(f'data_calendar_credit_allowance_current_value_: {data_calendar_credit_allowance_current_value_}')

            updated_credit_allowance = contract_credit_allowance + data_calendar_credit_allowance_current_value_

            # contract_credit_agreement_first_datetime = pd.to_datetime(contract_credit_agreement_first_datetime)
            # for row in temp_df.itertuples():
            #     temp_df_datetime = getattr(row, 'datetime')
            #
            #     temp_df_datetime = pd.to_datetime(temp_df_datetime)
            #     if temp_df_datetime>=contract_credit_agreement_first_datetime:
            #         output_object_list.append('да')






            # создаем новый временный df

            # output_object_list.append(f'contract_name: {contract_name}, contract_credit_allowance: {contract_credit_allowance}, contract_credit_agreement_first_date: {contract_credit_agreement_first_date}')
            df_result_list = []
            # список дат
            df_calendar_datetime_list = list(df_calendar_data['datetime'].unique())



            for calendar_datetime in df_calendar_datetime_list:
                temp_dict = {}
                # date = datetime.datetime.strptime(str(date), '%Y-%m-%d')
                # contract_credit_agreement_first_date = datetime.datetime.strptime(str(contract_credit_agreement_first_date), '%Y-%m-%d %H:%M:%S')
                calendar_datetime = pd.to_datetime(calendar_datetime)
                contract_credit_agreement_first_datetime = pd.to_datetime(contract_credit_agreement_first_datetime)

                temp_dict['calendar_datetime'] = calendar_datetime
                temp_dict['contract_name'] = contract_name
                temp_dict['credit_allowance'] = 0

                if calendar_datetime >= contract_credit_agreement_first_datetime:
                    # output_object_list.append('да')
                    temp_dict['credit_allowance'] = contract_credit_allowance

                # для каждого дня нужно получить значение задолженности
                dolg_value_df = 0
                try:
                    dolg_value_df = contract_df.loc[contract_df['date_time']>=calendar_datetime]
                except Exception as e:
                    output_object_list.append(f'ошибка при получении dolg_value_df: {e}')

                # dolg_value = dolg_value_df['amount'].sum()
                # temp_dict['dolg_value'] = dolg_value


                df_result_list.append(temp_dict)


            temp_df = pd.DataFrame(df_result_list)
            credit_limit_data_df = pd.concat([credit_limit_data_df, temp_df])


        data_calendar = credit_limit_data_df.to_dict('records')
        datatable_2 = dash_table.DataTable(data=data_calendar, )

        data = contract_df.to_dict('records')
        credit_datatable = dash_table.DataTable(data=data, )

        taken_vs_remain_v2_func_check_ = html.Div(
            children=[

                str(date_record_temp),
                html.Div(
                    children=output_object_list
                ),
                datatable_2,
                credit_datatable
            ]
        )

        # output = fig_div
        return output, taken_vs_remain_v2_func_check_



        #
        # # итерируемся по договорам для включения ограничений по срокам лимитов
        # agreement_list = list(df_credit_main['contract_title'].unique())
        # df_tranch_data_credit_limit = pd.DataFrame()
        # df_tranch_data_merged = pd.DataFrame()
        #
        # for contract_name in agreement_list:
        #     ######################################## credit payments ##########################################
        #     ###################################################################################################
        #     contract_df = df_credit_main.loc[df_credit_main['contract_title'] == str(contract_name)]
        #     payments_filtered_df = contract_df.loc[contract_df['credit_line_type'] == 'Возобновляемая']
        #     date_payments_df = payments_filtered_df.groupby(['date'], as_index=False).agg({'amount': 'sum'})
        #     date_payments_df['date_date'] = pd.to_datetime(date_payments_df['date']).dt.date
        #
        #     df_tranch_data_payments = df_tranch_data.merge(date_payments_df, left_on='date', right_on='date_date',
        #                                                    how='left')
        #     df_tranch_data_payments['amount'].fillna(0, inplace=True)
        #     df_tranch_data_payments['amount'] = df_tranch_data_payments['amount'].replace('', 0)
        #     df_tranch_data_payments['credit_payments'] = df_tranch_data_payments['credit_payments'] + \
        #                                                  df_tranch_data_payments['amount']
        #     df_tranch_data_payments.rename(columns={
        #         'date_x': 'date'
        #     }, inplace=True)
        #
        #     df_tranch_data_payments['credit_payments_cumulative'] = df_tranch_data_payments['credit_payments'].cumsum()
        #     df_tranch_data_payments['payments_cumulative'] = df_tranch_data_payments['payments_cumulative'] + df_tranch_data_payments['credit_payments_cumulative']
        #
        #     ################# получаем колонку с payments_before_today ####################
        #     df_tranch_data_payments['payments_cumulative_before_today_agreement'] = df_tranch_data_payments['payments_cumulative']
        #     df_tranch_data_payments.loc[df_tranch_data_payments['date']>=datetime.datetime.now().date(), ['payments_cumulative_before_today_agreement']] = 0
        #     df_tranch_data_payments['payments_cumulative_before_today'] = df_tranch_data_payments['payments_cumulative_before_today'] + df_tranch_data_payments['payments_cumulative_before_today_agreement']
        #
        #     ################# получаем колонку с payments_after_today ####################
        #     df_tranch_data_payments['payments_cumulative_after_today_agreement'] = df_tranch_data_payments['payments_cumulative']
        #     df_tranch_data_payments.loc[df_tranch_data_payments['date'] < datetime.datetime.now().date(), [
        #         'payments_cumulative_after_today_agreement']] = 0
        #     df_tranch_data_payments['payments_cumulative_after_today'] = df_tranch_data_payments['payments_cumulative_after_today'] + df_tranch_data_payments[
        #                                                                       'payments_cumulative_after_today_agreement']
        #
        #     ################# получаем колонку с payments_flat_after_today ####################
        #     df_tranch_data_payments['payments_flat_after_today_agreement'] = df_tranch_data_payments[
        #         'payments_cumulative']
        #     # получаем последнее значение в payments_before_today
        #     max_payment_cumulative_value = df_tranch_data_payments['payments_cumulative_before_today'].max()
        #
        #
        #     df_tranch_data_payments.loc[df_tranch_data_payments['date'] >= datetime.datetime.now().date(), ['payments_flat_after_today_agreement']] = max_payment_cumulative_value
        #     df_tranch_data_payments['payments_flat_after_today'] = df_tranch_data_payments['payments_flat_after_today'] + df_tranch_data_payments['payments_flat_after_today_agreement']
        #
        #     df_tranch_data = df_tranch_data_payments.loc[:,
        #                      ['date', 'allowance', 'allowance_cumulative', 'credit_tranch', 'tranch_cumulative',
        #                       'credit_payments', 'payments_cumulative', 'payments_cumulative_before_today',
        #                       'payments_cumulative_after_today', 'payments_flat_after_today', 'credit_limit_cumulative'
        #                       ]]
        #
        # ##################################### credit tranches ########################################
        # ###############################################################################################
        # for contract_name in agreement_list:
        #     contract_df = df_credit_main.loc[df_credit_main['contract_title'] == str(contract_name)]
        #     # получаем список траншей в выборке по договору
        #     tranch_list_in_contract = list(contract_df['transh_id'].unique())
        #     # внутри выборки по договору итерируемся по траншам
        #     for tranch in tranch_list_in_contract:
        #         temp_tranch_df = contract_df.loc[contract_df['transh_id'] == tranch]
        #         # дата транша
        #         tranch_date = temp_tranch_df.iloc[0, temp_tranch_df.columns.get_loc("credit_tranch_date")]
        #
        #         creditor = temp_tranch_df.iloc[0, temp_tranch_df.columns.get_loc("creditor")]
        #         tranch_volume = temp_tranch_df.iloc[0, temp_tranch_df.columns.get_loc("credit_amount")]
        #
        #         # Обновляем данные в df_tranch_data
        #         current_tranch_volume_value = df_tranch_data.loc[df_tranch_data['date'] == tranch_date.date(), ['credit_tranch']]
        #         updated_tranch_volume_value = current_tranch_volume_value + tranch_volume
        #         df_tranch_data.loc[df_tranch_data['date'] == tranch_date.date(), ['credit_tranch']] = updated_tranch_volume_value
        #
        #     # получаем колонку с накопительным итогом траншей
        # df_tranch_data['tranch_cumulative'] = df_tranch_data['credit_tranch'].cumsum()
        #
        #
        # for contract_name in agreement_list:
        #     contract_df = df_credit_main.loc[df_credit_main['contract_title'] == str(contract_name)]
        #     ##################################### credit allowance ########################################
        #     ###############################################################################################
        #     date_allowance_df = contract_df.groupby(['credit_agreement_first_date'], as_index=False).agg({'credit_agreement_total_volume': 'max'})
        #
        #     df_tranch_data_credit_limit = df_tranch_data.merge(date_allowance_df, left_on='date', right_on='credit_agreement_first_date', how='left')
        #
        #     df_tranch_data_credit_limit['credit_agreement_total_volume'].fillna(0, inplace=True)
        #     df_tranch_data_credit_limit['credit_agreement_total_volume'] = df_tranch_data_credit_limit['credit_agreement_total_volume'].replace('', 0)
        #
        #     df_tranch_data_credit_limit['allowance_cumulative_agreement_cumsum'] = df_tranch_data_credit_limit['credit_agreement_total_volume'].cumsum()
        #
        #     df_tranch_data_credit_limit['credit_limit_agreement'] = df_tranch_data_credit_limit['allowance_cumulative_agreement_cumsum']
        #
        #     df_tranch_data_credit_limit['allowance_cumulative'] = df_tranch_data_credit_limit['allowance_cumulative'] + df_tranch_data_credit_limit['allowance_cumulative_agreement_cumsum']
        #
        #     # df_tranch_data_credit_limit['credit_limit_agreement'] = df_tranch_data_credit_limit['allowance_cumulative_agreement_cumsum'] +
        #     # df_tranch_data_credit_limit['credit_limit'] = df_tranch_data_credit_limit['credit_limit'] +df_tranch_data_credit_limit['payments_flat_after_today']
        #
        #     ###################################  ral_credit_transh_getting_deadline ##############################
        #     ral_credit_transh_getting_deadline = contract_df.iloc[0]['ral_credit_transh_getting_deadline']
        #     """type: datetime"""
        #     ral_credit_transh_getting_deadline_date = ral_credit_transh_getting_deadline.date()
        #     """type: date"""
        #
        #     limitdeadline = contract_df.iloc[0]['limitdeadline']
        #     """type: datetime"""
        #     limitdeadline_date = limitdeadline.date()
        #     """type: date"""
        #
        #     # ral_credit_transh_getting_deadline = datetime.datetime(2023,2,1)
        #     # limitdeadline_date = datetime.datetime(2023, 3, 27).date()
        #
        #     credit_limit_df_min_date = df_tranch_data_credit_limit['date'].min()
        #     credit_limit_df_max_date = df_tranch_data_credit_limit['date'].max()
        #
        #     if ral_credit_transh_getting_deadline_date >= credit_limit_df_min_date and ral_credit_transh_getting_deadline_date <= credit_limit_df_max_date:
        #         if ral_credit_transh_getting_deadline_date < limitdeadline_date:
        #             # рассчитываем сумму задолжености как разницу значения tranch_cumulative и payments_cumulative
        #             ral_credit_transh_getting_deadline_tranch_cumulative_value_df = df_tranch_data_credit_limit.loc[df_tranch_data_credit_limit['date'] == ral_credit_transh_getting_deadline_date]
        #
        #             ral_credit_transh_getting_deadline_tranch_cumulative_value = ral_credit_transh_getting_deadline_tranch_cumulative_value_df.iloc[0]['tranch_cumulative']
        #
        #             ral_credit_transh_getting_deadline_payments_cumulative_value = ral_credit_transh_getting_deadline_tranch_cumulative_value_df.iloc[0]['payments_cumulative']
        #
        #             dolg_amount = ral_credit_transh_getting_deadline_tranch_cumulative_value - ral_credit_transh_getting_deadline_payments_cumulative_value
        #
        #             df_tranch_data_credit_limit.loc[df_tranch_data_credit_limit['date'] > ral_credit_transh_getting_deadline_date, [
        #                 'credit_limit_agreement']] = dolg_amount
        #
        #
        #     # обнуление значений после даты limitdeadline_date
        #     df_tranch_data_credit_limit.loc[df_tranch_data_credit_limit['date'] > limitdeadline_date, ['credit_limit_agreement']] = 0
        #
        #     df_tranch_data_credit_limit['credit_limit_cumulative'] = df_tranch_data_credit_limit['credit_limit_cumulative'] + df_tranch_data_credit_limit['credit_limit_agreement']
        #
        #
        #     df_tranch_data = df_tranch_data_credit_limit.loc[:,
        #                      ['date', 'allowance', 'allowance_cumulative', 'credit_tranch', 'tranch_cumulative',
        #                       'credit_payments', 'payments_cumulative', 'payments_cumulative_before_today',
        #                       'payments_cumulative_after_today', 'payments_flat_after_today', 'credit_limit_cumulative'
        #                       ]]
        #
        #
        #
        #
        # ##### ЗНАЧЕНИЕ tranch_cumulative в 1 января текущего года ##################
        # tranch_cumulative_1_st_jan_df = df_tranch_data.loc[df_tranch_data['date']==current_year_first_date.date(), ['tranch_cumulative']]
        # tranch_cumulative_1_st_jan = tranch_cumulative_1_st_jan_df.iloc[0]['tranch_cumulative']
        #
        # # вычитаем из траншей
        # df_tranch_data['tranch_cumulative_current_year'] = df_tranch_data['tranch_cumulative'] - tranch_cumulative_1_st_jan
        #
        # # вычитаем из лимитов
        # df_tranch_data['allowance_cumulative_current_year'] = df_tranch_data['allowance_cumulative'] - tranch_cumulative_1_st_jan
        #
        # df_tranch_data_graph = df_tranch_data.loc[df_tranch_data['date']>current_year_first_date.date()]
        #
        # df_tranch_data_graph.loc[df_tranch_data_graph['date']>datetime.datetime.now().date(), ['tranch_cumulative_current_year']] = 0
        #
        # y_tranch_raw_list = list(df_tranch_data_graph['tranch_cumulative_current_year'] / 1000000000)
        # y_tranch_rounded_value_list = []
        # for x in y_tranch_raw_list:
        #     x_rounded = rd(x, 3)
        #     y_tranch_rounded_value_list.append(x_rounded)
        #
        # y_limit_raw_list = list(df_tranch_data_graph['allowance_cumulative_current_year'] / 1000000000)
        # y_limit_rounded_value_list = []
        # for x in y_limit_raw_list:
        #     x_rounded = rd(x, 3)
        #     y_limit_rounded_value_list.append(x_rounded)
        #



        # fig = go.Figure()
        # x_tranch = df_tranch_data_graph['date']
        # y_tranch = y_tranch_rounded_value_list
        #
        # x_limit = df_tranch_data_graph['date']
        # y_limit = y_limit_rounded_value_list
        #
        # fig.add_trace(go.Scatter(x=x_tranch, y=y_tranch, name='Транши', fill='tozeroy', line={'color': '#FFC000'}))
        # fig.add_trace(go.Scatter(x=x_limit, y=y_limit, name='Лимиты',
        #                          # fill='tonexty'
        #                          ))
        #
        #
        # fig.add_vline(
        #     x=datetime.datetime.now(),
        #     # line_width=3,
        #     # line_dash="dash",
        #     line_color="#32935F")
        #
        # fig.update_layout(
        #     # title='Транши и лимиты',
        #     margin=dict(l=5, r=5, t=75, b=5),
        # )
        # fig.update_layout(
        #     {
        #         'legend': {
        #             'orientation': "h",
        #             'yanchor': "bottom",
        #             'y': 1.08,
        #         }
        #     }
        # )
        # fig.update_traces(
        #     mode="lines",
        #     # hovertemplate=None
        # )
        # fig.update_layout(hovermode="x unified")
        #
        # fig_div = dcc.Graph(figure=fig, config={'displayModeBar': False})



        # data_2 = df_tranch_data_merged.to_dict('records')
        # datatable_df_tranch_data_ = dash_table.DataTable(data=data_2, )


