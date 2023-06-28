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

        # создаем payment_id
        df_credit_main['payment_id'] = df_credit_main['transh_id'].astype(str) + '_payment_' + df_credit_main['date'].astype(str)


        calendar_df = pd.DataFrame()
        for contract_name in agreement_list:
            result_df_list = []
            contract_df = df_credit_main.loc[df_credit_main['contract_title'] == str(contract_name)]

            creditor = contract_df.iloc[0]['creditor']
            credit_agreement_first_date = contract_df.iloc[0]['credit_agreement_first_date']
            credit_agreement_first_datetime = contract_df.iloc[0]['credit_agreement_first_datetime']
            credit_agreement_total_volume = contract_df.iloc[0]['credit_agreement_total_volume']

            # получаем список траншей в данном договоре
            transh_list = list(contract_df['transh_id'].unique())

            for transh_id in transh_list:

                tranch_agreement_df = contract_df.loc[contract_df['transh_id']==str(transh_id)]

                tranch_date = datetime.datetime(2050,1,1)
                tranch_volume = 0
                try:
                    tranch_date = tranch_agreement_df['credit_tranch_date'].min()
                    # tranch_date = tranch_agreement_df.iloc[0]['credit_tranch_date']
                    # tranch_volume = tranch_agreement_df.iloc[0]['credit_amount']
                    tranch_volume = tranch_agreement_df['credit_amount'].max()


                except Exception as e:
                    output_object_list.append(f'tranch_date error {e}')

                tranch_date_date = tranch_date.date()

                # получаем список платежей в данном транше
                payments_in_transh_list = list(contract_df['payment_id'].unique())

                output_object_list.append(str(payments_in_transh_list))
                # итерируемся по платежам, входящим в данный транш
                # try:
                #     for payment_id in payments_in_transh_list:
                #         payments_transh_df = tranch_agreement_df.loc[tranch_agreement_df['payment_id']==str(payment_id)]
                # except Exception as e:
                #     output_object_list.append(f'payments_transh_df error {e}')




                # в колонку credit_agreement_total_volume записывается объем кредита по договору в первом дне (для суммирования в groupby)
                # в колонку credit_agreement_total_volume_by_days записываем объем кредита во все дни после первого дня
                for row in df_calendar_data.itertuples():
                    temp_dict = {}
                    df_calendar_data_date = getattr(row, 'date')
                    temp_dict['date'] = df_calendar_data_date
                    if df_calendar_data_date==credit_agreement_first_date:
                        temp_dict['creditor'] = creditor
                        temp_dict['agreement'] = contract_name
                        temp_dict['credit_agreement_first_date'] = credit_agreement_first_date
                        temp_dict['credit_agreement_total_volume'] = credit_agreement_total_volume
                        temp_dict['credit_agreement_total_volume_by_days'] = credit_agreement_total_volume
                    elif  df_calendar_data_date>credit_agreement_first_date:
                        temp_dict['creditor'] = creditor
                        temp_dict['agreement'] = contract_name
                        temp_dict['credit_agreement_first_date'] = credit_agreement_first_date
                        temp_dict['credit_agreement_total_volume'] = 0
                        temp_dict['credit_agreement_total_volume_by_days'] = credit_agreement_total_volume
                    else:
                        temp_dict['creditor'] = creditor
                        temp_dict['agreement'] = contract_name
                        temp_dict['credit_agreement_first_date'] = datetime.datetime(2050,1 ,1).date()
                        temp_dict['credit_agreement_total_volume'] = 0
                        temp_dict['credit_agreement_total_volume_by_days'] = 0

                    if df_calendar_data_date == tranch_date_date:
                        temp_dict['transh_id'] = transh_id
                        temp_dict['tranch_date_date'] = tranch_date_date
                        temp_dict['tranch_volume'] = tranch_volume
                        temp_dict['tranch_volume_by_days'] = tranch_volume

                    elif df_calendar_data_date > tranch_date_date:
                        temp_dict['transh_id'] = transh_id
                        temp_dict['tranch_date_date'] = tranch_date_date
                        temp_dict['tranch_volume'] = 0
                        temp_dict['tranch_volume_by_days'] = tranch_volume
                    else:
                        temp_dict['transh_id'] = transh_id
                        temp_dict['tranch_date_date'] = datetime.datetime(2050,1 ,1).date()
                        temp_dict['tranch_volume'] = 0
                        temp_dict['tranch_volume_by_days'] = 0




                    result_df_list.append(temp_dict)

            agreement_calendar_df = pd.DataFrame(result_df_list)
            calendar_df = pd.concat([calendar_df, agreement_calendar_df])


        one_bank_calendar_df = calendar_df.loc[calendar_df['creditor']== 'СМП БАНК АО']
        one_bank_calendar_df = one_bank_calendar_df.groupby(['date', 'creditor','tranch_date_date', 'transh_id'], as_index=False).agg({'tranch_volume': 'sum'})
        # transh_sum = calendar_df['tranch_volume'].sum()


        calendar_df.sort_values(['creditor','date',], inplace=True, ignore_index=True)
        # data = calendar_df.to_dict('records')
        data = one_bank_calendar_df.to_dict('records')
        output_object_list.append(f'cmp tranch {one_bank_calendar_df["tranch_volume"].sum()}')
        credit_datatable = dash_table.DataTable(data=data, )

        output = html.Div(
            children=[
                html.Div(
                    children=output_object_list
                ),
                credit_datatable
            ]
        )



    return output