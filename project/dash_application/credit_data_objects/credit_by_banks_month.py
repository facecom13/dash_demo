import os
from sqlalchemy import create_engine
import pandas as pd
import datetime
import re
from dash import dash_table
from dash import html

def credit_by_banks_month_func(data_input, transhi_i_crediti_block_creditor_select):

    output = ""
    output_object_list = []
    if data_input == '1с_api':
        url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
        engine = create_engine(url_db, pool_recycle=3600)
        with engine.connect() as con:
            # query = 'SELECT *  FROM "creditDB";'
            query = 'SELECT *  FROM "creditdb_2";'
            df_credit_main = pd.read_sql(query, con)



        with engine.connect() as con:
            # query = 'SELECT *  FROM "creditDB";'
            query_creditnewdata = 'SELECT *  FROM "creditnewdata";'
            try:
                df_creditnewdata = pd.read_sql(query_creditnewdata, con)
            except Exception as e:
                output_object_list.append(f'df_creditnewdata: {e}')

        df_credit_main['type'] = 'main'
        df_creditnewdata['type'] = 'added'
        df_credit_main = pd.concat([df_credit_main, df_creditnewdata])

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







        df_credit_main['agreement_code'].fillna('Кредиты', inplace=True)
        df_credit_main['agreement_code'] = df_credit_main['agreement_code'].replace(r'', 'Кредиты', regex=True)

        df_credit_main  = df_credit_main.loc[df_credit_main['agreement_code']=='Кредиты']



        df_credit_main['credit_volume'].fillna(0, inplace=True)
        df_credit_main['credit_volume'] = df_credit_main['credit_volume'].replace('', 0, regex=True)

        df_credit_main['amount'].fillna(0, inplace=True)
        df_credit_main['amount'] = df_credit_main['amount'].replace('', 0, regex=True)

        df_credit_main['credit_tranch_date'].fillna(datetime.datetime(2050, 1, 1), inplace=True)
        df_credit_main['credit_tranch_date'] = df_credit_main['credit_tranch_date'].replace('',
                                                                                            datetime.datetime(2050, 1,
                                                                                                              1),
                                                                                            regex=True)
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



        # итерируемся по договорам

        agreement_list = list(df_credit_main['contract_title'].unique())

        all_agreements_df = pd.DataFrame()
        payment_agreement_selected_df = pd.DataFrame()
        agreement_calendar_df = pd.DataFrame()
        refunded_payments_df = pd.DataFrame()
        all_transh_df = pd.DataFrame()
        """ в all_agreements_df - все записи по дням по всем договорам """
        for agreement in agreement_list:
            agreement_df = df_credit_main.loc[df_credit_main['contract_title'] == str(agreement)]

            creditor = agreement_df.iloc[0, agreement_df.columns.get_loc("creditor")]

            contract_title = agreement_df.iloc[0, agreement_df.columns.get_loc("contract_title")]

            credit_agreement_total_volume = agreement_df.iloc[0, agreement_df.columns.get_loc("credit_agreement_total_volume")]

            credit_agreement_first_datetime = agreement_df.iloc[0, agreement_df.columns.get_loc("credit_agreement_first_datetime")]

            credit_tranch_date = agreement_df.iloc[0, agreement_df.columns.get_loc("credit_tranch_date")]
            credit_tranch_date_min = agreement_df['credit_tranch_date'].min()
            """type: datetime"""

            # дата начала действия договора
            agreement_start_datetime = min ([credit_agreement_first_datetime, credit_tranch_date_min])
            agreement_df['agreement_start_datetime'] = agreement_start_datetime
            # дата конца действия договора
            agreement_finish_datetime = agreement_df['date'].max()

            ral_credit_transh_getting_deadline = agreement_df.iloc[0, agreement_df.columns.get_loc("ral_credit_transh_getting_deadline")]
            limitdeadline = agreement_df.iloc[0, agreement_df.columns.get_loc("limitdeadline")]
            credit_line_type = agreement_df.iloc[0, agreement_df.columns.get_loc("credit_line_type")]
            freelimitremainings = agreement_df.iloc[0, agreement_df.columns.get_loc("freelimitremainings")]
            # получаем дату последнего платежа во всем массиве
            df_credit_credit_payments = df_credit_main.loc[df_credit_main['date'] != datetime.datetime(2050, 1, 1)]
            last_payment_datetime = df_credit_credit_payments['date'].max()

            if agreement_finish_datetime == datetime.datetime(2050, 1, 1):
                agreement_finish_datetime = last_payment_datetime


            # создаем массив строк по датам от начала действия договора до конца
            df_result_list = []
            temp_date = agreement_start_datetime

            while temp_date <= agreement_finish_datetime:
                temp_dict = {}
                temp_dict['datetime'] = temp_date
                temp_dict['date'] = temp_date.date()
                temp_dict['creditor'] = creditor
                temp_dict['contract_title'] = contract_title
                temp_dict['credit_agreement_total_volume'] = credit_agreement_total_volume
                temp_dict['agreement_start_datetime'] = agreement_start_datetime
                temp_dict['agreement_finish_datetime'] = agreement_finish_datetime
                temp_dict['ral_credit_transh_getting_deadline'] = ral_credit_transh_getting_deadline
                temp_dict['limitdeadline'] = limitdeadline
                temp_dict['credit_line_type'] = credit_line_type
                temp_dict['freelimitremainings'] = freelimitremainings


                df_result_list.append(temp_dict)
                temp_date = temp_date + datetime.timedelta(days=1)


            agreement_calendar_df = pd.DataFrame(df_result_list)

            # после первого прохода и создания строк с лимитом нужно соединить таблицу с платежами
            # исключаем строки в agreement_df с 2050 году в поле date
            # payment_agreement_df = agreement_df.loc[agreement_df['date']!=datetime.datetime(2050, 1, 1)]


            # if len(payment_agreement_df)>0:

            agreement_df['payment_date'] = agreement_df['date'].dt.date
            payment_agreement_selected_df = agreement_df.loc[:, ['date', 'payment_date', 'amount']]

            # сгруппировываем по дате
            payments_groupped = payment_agreement_selected_df.groupby(['payment_date'], as_index=False).agg({'amount': 'sum'})
            agreement_calendar_df = agreement_calendar_df.merge(payments_groupped, how='left', left_on='date', right_on='payment_date')

            agreement_calendar_df.rename(columns={
                'date_x': 'date'
            }, inplace=True)

            agreement_calendar_df['amount'].fillna(0, inplace=True)
            agreement_calendar_df['amount'] = agreement_calendar_df['amount'].replace('', 0, regex=True)
            agreement_calendar_df['amount_minus'] = agreement_calendar_df['amount'] * -1
            agreement_calendar_df['payments_cumsum'] = agreement_calendar_df['amount_minus'].cumsum()

            # аналогично соединяем с данными по траншам
            tranch_result_list = []
            tranch_list = list(agreement_df['transh_id'].unique())


            agreement_transh_df = agreement_df.loc[agreement_df['credit_tranch_date']!=datetime.datetime(2050, 1, 1)]
            for transh_id in tranch_list:
                temp_dict = {}
                tranche_data_df = agreement_transh_df.loc[agreement_transh_df['transh_id'] == str(transh_id)]
                # tranche_data_df = tranche_data_df.reset_index(drop=True)
                tranch_volume = tranche_data_df['credit_volume'].max()
                transh_date = tranche_data_df['credit_tranch_date'].max()
                temp_dict['creditor'] = creditor
                temp_dict['contract_title'] = contract_title
                temp_dict['transh_id'] = transh_id
                temp_dict['transh_date'] = transh_date
                temp_dict['tranch_volume'] = tranch_volume

                tranch_result_list.append(temp_dict)

            transh_df = pd.DataFrame(tranch_result_list)
            transh_df['transh_date_date'] = transh_df['transh_date'].dt.date

            agreement_calendar_df['date_merge'] = agreement_calendar_df['date'].astype(str)
            transh_df['date_merge'] = transh_df['transh_date_date'].astype(str)

            transh_df_selected = transh_df.loc[:, ['date_merge', 'transh_date_date', 'transh_date', 'transh_id', 'tranch_volume']]

            # сгруппировываем по дате
            transhes_groupped = transh_df_selected.groupby(['date_merge'], as_index=False).agg({'tranch_volume': 'sum'})

            agreement_calendar_df = agreement_calendar_df.merge(transhes_groupped, how='left', left_on='date_merge', right_on='date_merge')

            agreement_calendar_df.rename(columns={
                'date_x': 'date'
            }, inplace=True)

            agreement_calendar_df['tranch_volume'].fillna(0, inplace=True)
            agreement_calendar_df['tranch_volume'] = agreement_calendar_df['tranch_volume'].replace('', 0, regex=True)
            agreement_calendar_df['transh_cumsum'] = agreement_calendar_df['tranch_volume'].cumsum()


            ######## ДОЛГ
            agreement_calendar_df['dolg'] = agreement_calendar_df['transh_cumsum'] + agreement_calendar_df['payments_cumsum']

            agreement_calendar_df['limit_date'] = agreement_calendar_df['limitdeadline'].dt.date
            agreement_calendar_df['ral_limit_date'] = agreement_calendar_df['ral_credit_transh_getting_deadline'].dt.date

            result_list = []
            for row in agreement_calendar_df.itertuples():
                temp_dict = {}
                current_date = getattr(row, 'date')
                limit_date = getattr(row, 'limit_date')
                ral_limit_date = getattr(row, 'ral_limit_date')
                dolg = getattr(row, 'dolg')
                temp_dict['date'] = current_date
                credit_agreement_total_volume = getattr(row, 'credit_agreement_total_volume')

                if current_date < ral_limit_date:
                    temp_dict['credit_limit'] = credit_agreement_total_volume
                if current_date >= ral_limit_date and  current_date < limit_date:
                    temp_dict['credit_limit'] = dolg
                if current_date >= limit_date:
                    temp_dict['credit_limit'] = 0

                result_list.append(temp_dict)

            credit_limit_df = pd.DataFrame(result_list)
            credit_limit_df['date_merge'] = credit_limit_df['date'].astype(str)

            agreement_calendar_df = agreement_calendar_df.merge(credit_limit_df, how='left', left_on='date_merge',
                                                                right_on='date_merge')
            agreement_calendar_df.rename(columns={
                'date_x': 'date'
            }, inplace=True)
                    # output_object_list.append(str(current_date))


            # Возобновляемые payments
            result_list = []
            for row in agreement_calendar_df.itertuples():
                temp_dict = {}
                current_date = getattr(row, 'date')
                credit_line_type = getattr(row, 'credit_line_type')
                payments_cumsum = getattr(row, 'payments_cumsum')
                temp_dict['date'] = current_date

                if credit_line_type == 'Возобновляемая':
                    temp_dict['payment_correct_credit_limit'] = payments_cumsum * -1
                else:
                    temp_dict['payment_correct_credit_limit'] = 0
                result_list.append(temp_dict)
            refunded_payments_df = pd.DataFrame(result_list)


            refunded_payments_df['date_merge'] = refunded_payments_df['date'].astype(str)

            agreement_calendar_df = agreement_calendar_df.merge(refunded_payments_df, how='left', left_on='date_merge',
                                                                right_on='date_merge')

            agreement_calendar_df.rename(columns={
                'date_x': 'date'
            }, inplace=True)

            agreement_calendar_df.rename(columns={
                'amount_y': 'payment'
            }, inplace=True)

            agreement_calendar_df['free_remaining'] = agreement_calendar_df['credit_limit'] -agreement_calendar_df['transh_cumsum']+agreement_calendar_df['payment_correct_credit_limit']


            all_transh_df = pd.concat([all_transh_df, transh_df])



            all_agreements_df = pd.concat([all_agreements_df, agreement_calendar_df])
        return all_agreements_df
