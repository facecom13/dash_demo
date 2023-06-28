import os
from sqlalchemy import create_engine
import pandas as pd
import datetime
import re
from dash import dash_table
from dash import html

def credit_calendar_to_bd_func(data_input):

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

        df_credit_main = pd.concat([df_credit_main, df_creditnewdata])



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


        #################################################################################################
        # получаем дату последнего платежа во всем массиве
        df_credit_credit_payments = df_credit_main.loc[df_credit_main['date'] != datetime.datetime(2050, 1, 1)]
        last_payment_datetime = df_credit_credit_payments['date'].max()
        credit_agreement_first_datetime_min = df_credit_main['credit_agreement_first_datetime'].min()
        df_result_list = []
        temp_date = pd.to_datetime(credit_agreement_first_datetime_min)
        # output_object_list.append(f'credit_agreement_first_datetime_min {credit_agreement_first_datetime_min}')
        while temp_date <= last_payment_datetime:
            temp_dict = {}
            temp_dict['datetime'] = temp_date
            temp_dict['date'] = temp_date.date()
            temp_dict['credit_allowance'] = 0

            df_result_list.append(temp_dict)
            temp_date = temp_date + datetime.timedelta(days=1)

        df_calendar_data = pd.DataFrame(df_result_list)

        # данные по задолженности
        # задолженность - это
        df_credit_main['dolg']=0
        df_credit_main.sort_values(['date'], inplace=True)
        for row in df_credit_main.itertuples():
            creditor = getattr(row, 'creditor')
            current_date = getattr(row, 'date')
            transh_id = getattr(row, 'transh_id')
            dolg_transh_df = df_credit_main.loc[df_credit_main['transh_id']==transh_id]
            dolg_transh_after_current_date_df = dolg_transh_df.loc[dolg_transh_df['date']>current_date]

            dolg = dolg_transh_after_current_date_df['amount'].sum()
            index = getattr(row, 'Index')
            df_credit_main.loc[index, ['dolg']] = dolg





        # ряд кредитного лимита

        # df_credit_main_merged = pd.concat([df_credit_main, df_creditnewdata])

        df_credit_main['dolg'].fillna(0, inplace=True)
        df_credit_main['dolg'] = df_credit_main['dolg'] .replace('', 0, regex=True)

        credit_limit_df = df_credit_main.loc[:, ['creditor','credit_agreement_first_datetime','credit_agreement_first_date', 'contract_title', 'credit_agreement_total_volume', 'credit_line_type', 'limitdeadline', 'ral_credit_transh_getting_deadline','transh_id', 'dolg']]





        agreement_list = list(df_credit_main['contract_title'].unique())
        result_df = pd.DataFrame()
        try:
            result_df_list = []
            for agreement in agreement_list:
                agreement_df = df_credit_main.loc[df_credit_main['contract_title'] == str(agreement)]
                contract_title_text = agreement_df.iloc[0]['contract_title']
                creditor = agreement_df.iloc[0]['creditor']
                credit_agreement_first_date = agreement_df.iloc[0]['credit_agreement_first_date']
                credit_agreement_last_date = agreement_df['date'].max()
                credit_allowance = agreement_df.iloc[0]['credit_agreement_total_volume']

                agreement_limitdeadline = agreement_df['limitdeadline'].min()

                for row_df_calendar_data in df_calendar_data.itertuples():
                    temp_dict = {}
                    df_calendar_data_date = getattr(row_df_calendar_data, 'date')


                    # output_object_list.append(str(type(credit_agreement_first_date)))

                    if df_calendar_data_date == credit_agreement_first_date:
                        # output_object_list.append(str(type(credit_agreement_first_date)))
                        temp_dict['calendar_date'] = df_calendar_data_date
                        temp_dict['creditor'] =creditor
                        temp_dict['credit_agreement_first_date'] = credit_agreement_first_date
                        temp_dict['credit_agreement_last_datetime'] = credit_agreement_last_date
                        temp_dict['credit_agreement_last_date'] = credit_agreement_last_date.date()
                        temp_dict['credit_allowance'] = credit_allowance
                        temp_dict['agreement_limitdeadline'] = agreement_limitdeadline


                    result_df_list.append(temp_dict)
                #
                #
                #         output_object_list.append(credit_agreement_first_date)




            result_df = pd.DataFrame(result_df_list)
        except Exception as e:
            output_object_list.append(e)
        # for row in df_calendar_data.itertuples():
        #     df_calendar_data_datetime = getattr(row, 'datetime')
        #     df_calendar_data_date = getattr(row, 'date')






        # создаем таблицу credit_allowance
        try:
            if_exists = 'replace'
            with engine.connect() as con:
                result_df.to_sql(
                    name='credit_allowance',
                    con=con,
                    # chunksize=1000,
                    # method='multi',
                    index=False,
                    if_exists=if_exists
                )
        except:
            status_text = "не получилось создать таблицу credit_allowance"
            output_object_list.append(status_text)

        ############ создаем таблицу траншей
        result_tranch_df_list = []
        try:

            tranch_list = list(df_credit_main['transh_id'].unique())

            for tranch in tranch_list:
                temp_dict = {}
                temp_tranch_df = df_credit_main.loc[df_credit_main['transh_id'] == str(tranch)]
                creditor = temp_tranch_df.iloc[0, temp_tranch_df.columns.get_loc("creditor")]
                tranch_id = tranch
                credit_amount = temp_tranch_df['credit_volume'].max()
                agreement = temp_tranch_df.iloc[0, temp_tranch_df.columns.get_loc("credit_contract")]
                credit_line_type = temp_tranch_df.iloc[0, temp_tranch_df.columns.get_loc("credit_line_type")]
                transh_date = temp_tranch_df.iloc[0, temp_tranch_df.columns.get_loc("credit_tranch_date")]

                temp_dict['creditor'] = creditor
                temp_dict['tranch_id'] = tranch_id
                temp_dict['transh_date'] = transh_date
                temp_dict['credit_amount'] = credit_amount
                temp_dict['agreement'] = agreement
                temp_dict['credit_line_type'] = credit_line_type
                result_tranch_df_list.append(temp_dict)

        except:
            pass
        result_tranch_df = pd.DataFrame(result_tranch_df_list)

        try:
            if_exists = 'replace'
            with engine.connect() as con:
                result_tranch_df.to_sql(
                    name='credit_transhes',
                    con=con,
                    # chunksize=1000,
                    # method='multi',
                    index=False,
                    if_exists=if_exists
                )
        except:
            status_text = "не получилось создать таблицу credit_transhes"
            output_object_list.append(status_text)




        df_credit_main['payment_id'] = df_credit_main['transh_id'].astype(str) + "_payment_date" + df_credit_main['date'].astype(str)
        payment_id_list = list(df_credit_main['payment_id'].unique())

        for payment_id in payment_id_list:
            payment_df = df_credit_main.loc[df_credit_main['payment_id']==str(payment_id)]
            current_transh_id = payment_df.iloc[0, payment_df.columns.get_loc("transh_id")]
            current_credit_volume = payment_df.iloc[0, payment_df.columns.get_loc("credit_volume")]
            current_payment_date = payment_df.iloc[0, payment_df.columns.get_loc("date")]
            #объем платежей, которые произошли ранее
            temp_transh_df = df_credit_main.loc[df_credit_main['transh_id']==str(current_transh_id)]
            temp_payments_transh_df = temp_transh_df.loc[temp_transh_df['date']<=current_payment_date]
            payments_before_current_date = 0
            if len(temp_payments_transh_df)>0:
                # cтоимость всех платежей, которые были ранее
                payments_before_current_date = temp_payments_transh_df['amount'].sum()
            dolg = current_credit_volume - payments_before_current_date
            df_credit_main.loc[df_credit_main['payment_id']==str(current_transh_id), ['dolg']]=dolg
            # output_object_list.append(len(temp_payments_transh_df))

        try:
            if_exists = 'replace'
            with engine.connect() as con:
                df_credit_main.to_sql(
                    name='df_credit_main',
                    con=con,
                    # chunksize=1000,
                    # method='multi',
                    index=False,
                    if_exists=if_exists
                )
        except:
            status_text = "не получилось создать таблицу df_credit_main"
            output_object_list.append(status_text)


        # попытаемся заполнить таблицу календаря
        credit_limit_df_list = []
        for row in df_credit_main.itertuples():
            temp_dict = {}
            action_datetime = getattr(row, 'date')
            creditor = getattr(row, 'creditor')
            contract_title = getattr(row, 'contract_title')
            credit_agreement_total_volume = getattr(row, 'credit_agreement_total_volume')
            amount = getattr(row, 'amount')
            dolg = getattr(row, 'dolg')

            temp_dict['action_datetime'] = action_datetime
            temp_dict['creditor'] = creditor
            temp_dict['contract_title'] = contract_title
            temp_dict['credit_agreement_total_volume'] = credit_agreement_total_volume
            temp_dict['amount'] = amount
            temp_dict['dolg'] = dolg

            credit_limit_df_list.append(temp_dict)

        credit_limit_df = pd.DataFrame(credit_limit_df_list)

        data_temp = credit_limit_df.to_dict('records')
        datatable_credit_limit_df = dash_table.DataTable(data=data_temp, )
















        # dolg_df = pd.DataFrame()
        # agreement_list = list(df_credit_main['contract_title'].unique())
        # try:
        #     for agreement in agreement_list:
        #         agreement_df = df_credit_main.loc[df_credit_main['contract_title'] == str(agreement)]
        #         agreement_df = agreement_df.copy()
        #         agreement_df['date_date'] = agreement_df['date'].dt.date
        #         creditor = agreement_df.iloc[0, agreement_df.columns.get_loc("creditor")]
        #         credit_contract = agreement_df.iloc[0, agreement_df.columns.get_loc("contract_title")]
        #         ral_credit_transh_getting_deadline = agreement_df.iloc[0, agreement_df.columns.get_loc("ral_credit_transh_getting_deadline")]
        #         limitdeadline = agreement_df.iloc[0, agreement_df.columns.get_loc("limitdeadline")]
        #
        #         joined_df = pd.DataFrame()
        #         df_calendar_data.sort_values(['date'], inplace=True)
        #         agreement_df.sort_values('date_date', inplace=True)
        #
        #         try:
        #             joined_df = df_calendar_data.merge(agreement_df, left_on='date', right_on='date_date', how='left')
        #         except Exception as e:
        #             output_object_list.append(e)
        #
        #         joined_df.rename(columns={
        #             'date_x': 'date',
        #
        #         }, inplace=True)
        #         joined_df['credit_agreement_total_volume'].fillna(method='ffill', inplace=True)
        #         joined_df['credit_agreement_total_volume'] = joined_df['credit_agreement_total_volume'].replace('', 0, regex=True)
        #         joined_df['dolg'].fillna(method='ffill', inplace=True)
        #         joined_df['ral_credit_transh_getting_deadline'].fillna(method='ffill', inplace=True)
        #         joined_df['limitdeadline'].fillna(method='ffill', inplace=True)
        #         joined_df['contract_title'].fillna(method='ffill', inplace=True)
        #         # joined_df['dolg'] = joined_df['dolg'].replace('', 0, regex=True)
        #
        #         joined_df['creditor'].fillna(method='ffill', inplace=True)
        #
        #
        #         # joined_df['credit_contract'].fillna('delete', inplace=True)
        #         # joined_df['credit_contract'] = joined_df['credit_contract'].replace('','delete' , regex=True)
        #
        #         # joined_df = joined_df.loc[joined_df['credit_contract']!='delete']
        #
        #
        #         joined_df_selected = joined_df.loc[:, ['date','creditor', 'contract_title','credit_agreement_total_volume', 'amount','dolg', 'ral_credit_transh_getting_deadline', 'limitdeadline']]
        #
        #         dolg_df = pd.concat([dolg_df, joined_df_selected])
        #
        #
        #
        #
        # except Exception as e:
        #     output_object_list.append(e)
        #
        # # dolg_df.sort_values(['creditor', 'credit_contract', 'date'], inplace=True)
        #
        #
        # # прописываем значение лимита
        # dolg_df['credit_agreement_total_volume'].fillna(0, inplace=True)
        # dolg_df['credit_agreement_total_volume'] = dolg_df['credit_agreement_total_volume'].replace('',0 , regex=True)
        #
        # dolg_df['dolg'].fillna(0, inplace=True)
        # dolg_df['dolg'] = dolg_df['dolg'].replace('', 0, regex=True)
        #
        # # dolg_df = dolg_df.loc[dolg_df['credit_agreement_total_volume']!=0]
        #
        # list_of_agreements = list(dolg_df['contract_title'].unique())
        # # for agreement in list_of_agreements:
        # #     temp_agreement_df = dolg_df.loc[dolg_df['contract_title']==str(agreement)]
        # #     ral_credit_transh_getting_deadline = temp_agreement_df.iloc[0, temp_agreement_df.columns.get_loc("ral_credit_transh_getting_deadline")]
        # #     ral_credit_transh_getting_deadline = pd.to_datetime(ral_credit_transh_getting_deadline)
        #
        # df_result_list = []
        # for row in dolg_df.itertuples():
        #     temp_dict = {}
        #     credit_agreement_total_volume = getattr(row, 'credit_agreement_total_volume')
        #     current_date  = getattr(row, 'date')
        #     index_row = getattr(row, 'Index')
        #     ral_credit_transh_getting_deadline = getattr(row, 'ral_credit_transh_getting_deadline')
        #     creditor = getattr(row, 'creditor')
        #     dolg_value = getattr(row, 'dolg')
        #     amount = getattr(row, 'amount')
        #     contract_title = getattr(row, 'contract_title')
        #     ral_credit_transh_getting_deadline = pd.to_datetime(ral_credit_transh_getting_deadline)
        #
        #     limitdeadline = getattr(row, 'limitdeadline')
        #     # output_object_list.append(f"{dolg_df.columns.get_loc('credit_limit')}")
        #
        #     temp_dict['current_date'] = current_date
        #     temp_dict['creditor'] = creditor
        #     temp_dict['credit_agreement_total_volume'] = credit_agreement_total_volume
        #     temp_dict['dolg_value'] = dolg_value
        #     temp_dict['amount'] = amount
        #     temp_dict['contract_title'] = contract_title
        #     temp_dict['limitdeadline'] = limitdeadline
        #     temp_dict['ral_credit_transh_getting_deadline'] = ral_credit_transh_getting_deadline
        #
        #
        #
        #     if current_date < ral_credit_transh_getting_deadline.date():
        #         temp_dict['credit_limit'] = credit_agreement_total_volume
        #     if current_date >= ral_credit_transh_getting_deadline.date():
        #         temp_dict['credit_limit'] = dolg_value
        #
        #     if current_date >= limitdeadline.date():
        #         temp_dict['credit_limit'] = 0
        #
        #     df_result_list.append(temp_dict)
        #
        # updated_df = pd.DataFrame(df_result_list)
        #
        #         # dolg_df.iloc[index_row, dolg_df.columns.get_loc('credit_limit')] = credit_agreement_total_volume
        #     # elif current_date >= ral_credit_transh_getting_deadline.date():
        #     #     dolg_df.loc[index_row, ['credit_limit']] = dolg_value



        # data_joined_df = dolg_df.to_dict('records')
        # credit_datatable_joined_df = dash_table.DataTable(data=data_joined_df, )
        # output_object_list.append(credit_datatable_joined_df)






        data = df_credit_main.to_dict('records')
        credit_datatable = dash_table.DataTable(data=data, )

        output = html.Div(
            children=[
                html.Div(
                    children=output_object_list
                ),
                datatable_credit_limit_df,
                credit_datatable
            ]
        )

    return output