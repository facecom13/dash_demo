import datetime

import requests
from requests.auth import HTTPBasicAuth
import xmltodict
import pandas as pd
import json
from dash import dash_table
import io
from dash import html
import os
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
def credit_request_to_bd_func(data_input):
    output_mess = []
    status_text = ''
    status = 'ok'
    credit_datatable = ""
    output = ''
    data_input = '1с_api'
    if data_input == '1с_api':
        url = "http://ral-61.rosagroleasing.ru/work1cbuh_2_0/ws/GetDataFromReports.1cws"
        user = "UserGetDataFromReports"
        password = "Q!cmo7djz41rto"

        headers = {'content-type': 'text/xml'}
        body = f"""
                   <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:uri="uri.rosagroleasing.ru:GetDataFromReports">

                      <soapenv:Header/>

                      <soapenv:Body>

                         <uri:ГрафикиПогашенияКредитовИОблигацийВСтрочку>

                            <uri:ДатаНачала>2015-01-01</uri:ДатаНачала>

                            <uri:ДатаОкончания>2050-01-01</uri:ДатаОкончания>

                         </uri:ГрафикиПогашенияКредитовИОблигацийВСтрочку>

                      </soapenv:Body>

                   </soapenv:Envelope>
                   """
        body = body.encode('utf-8')
        credit_response = ''
        try:
            credit_response = requests.post(url, data=body, headers=headers, auth=HTTPBasicAuth(user, password))
        except Exception as credit_request_error:
            status_text = "Не удалось получить данные uri:ГрафикиПогашенияКредитовИОблигацийВСтрочку"
            status = 'failed_credit_request'
            output_mess.append(f'failed_credit_request {credit_request_error}')
            # return output, status

        dict_data = xmltodict.parse(credit_response.content.decode('utf-8'))
        data_credit = \
            dict_data['soap:Envelope']['soap:Body']['m:ГрафикиПогашенияКредитовИОблигацийВСтрочкуResponse'][
                'm:return']['#text']

        data_credit_raw_data = json.loads(data_credit)



        raw_credit_df = pd.DataFrame.from_records(data_credit_raw_data)
        df = raw_credit_df

        df.rename(columns={
            'Дата': 'date',

        }, inplace=True)
        df['date'] = df['date'].replace('', '01.01.2050 0:00:00')
        df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y %H:%M:%S')

        # создаем два df и две таблицы - старую и с новыми данными. Объединять будем по полю contract_title

        df_new_data = df.loc[df['date']==datetime.datetime(2050,1,1)]
        df_new_data.rename(columns={
            'Кредитор': 'creditor',
            'ВидДоговора': 'contract_title',
            'ОбщаяСуммаДоговора': 'credit_agreement_total_volume',
            'Дата': 'date',
            'ТипКредитнойЛинии': 'credit_line_type',
            'СвободныйОстатокЛимита': 'freelimitremainings',
            'СрокДействияЛимита': 'limitdeadline',
            'РАЛ_СрокПолученияТраншей':'ral_credit_transh_getting_deadline'

        }, inplace=True)
        df_new_data = df_new_data.copy()
        df_new_data['freelimitremainings'] = df_new_data['freelimitremainings'].str.replace(r'\u00A0', '', regex=True)
        df_new_data['freelimitremainings'] = df_new_data['freelimitremainings'].str.replace(r' ', '', regex=True)
        df_new_data['freelimitremainings'] = df_new_data['freelimitremainings'].str.replace(',', '.')
        df_new_data['freelimitremainings'] = df_new_data['freelimitremainings'].replace('', 0)
        df_new_data['freelimitremainings'] = df_new_data['freelimitremainings'].astype('float')

        df_new_data['credit_agreement_total_volume'] = df_new_data['credit_agreement_total_volume'].str.replace(r'\u00A0', '', regex=True)
        df_new_data['credit_agreement_total_volume'] = df_new_data['credit_agreement_total_volume'].str.replace(r' ', '', regex=True)
        df_new_data['credit_agreement_total_volume'] = df_new_data['credit_agreement_total_volume'].str.replace(',', '.')
        df_new_data['credit_agreement_total_volume'] = df_new_data['credit_agreement_total_volume'].replace('', 0)
        df_new_data['credit_agreement_total_volume'] = df_new_data['credit_agreement_total_volume'].astype('float')

        df_new_data['limitdeadline'] = df_new_data['limitdeadline'].replace('', '01.01.2050 0:00:00')
        df_new_data['limitdeadline'] = pd.to_datetime(df_new_data['limitdeadline'], format='%d.%m.%Y %H:%M:%S')

        df_new_data['ral_credit_transh_getting_deadline'] = df_new_data['ral_credit_transh_getting_deadline'].replace('', '01.01.2050 0:00:00')
        df_new_data['ral_credit_transh_getting_deadline'] = pd.to_datetime(df_new_data['ral_credit_transh_getting_deadline'], format='%d.%m.%Y %H:%M:%S')


        url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
        engine = sqlalchemy.create_engine(url_db)
        # создаем таблицу creditnewdata
        try:
            if_exists = 'replace'
            with engine.connect() as con:
                df_new_data.to_sql(
                    name='creditnewdata',
                    con=con,
                    # chunksize=1000,
                    # method='multi',
                    index=False,
                    if_exists=if_exists
                )
        except:
            status_text = "не получилось создать таблицу df_new_data"
            status = ''
            return status_text



        # data = df_new_data.to_dict('records')
        # credit_datatable = dash_table.DataTable(data=data, )


        df = df.loc[df['date']!=datetime.datetime(2050,1,1)]




        output = html.Div(
            children=[
                credit_datatable
            ]
        )


        # присваиваем идентификатор траншу кредита
        df['transh_id'] = df['Кредитор'] + "_" + df['ДатаТраншаКредита']

        df.rename(columns={
            'ОбщаяСуммаДоговора': 'credit_agreement_total_volume',
            'СуммаТраншаКредита': 'credit_volume',
            'ДатаТраншаКредита': 'credit_tranch_date',
            'ВидПлатежа': 'agreement_code',
            'Кредитор': 'creditor',
            'Договор': 'credit_contract',
            'ВидДоговора': 'contract_title',
            'Дата': 'date',
            'ЗначениеПлатежа': 'amount',
            'Ставка': 'credit_annual_rate',
            'ТипКредитнойЛинии': 'credit_line_type',
            'СвободныйОстатокЛимита': 'freelimitremainings',
            'СрокДействияЛимита': 'limitdeadline',
            'РАЛ_СрокПолученияТраншей': 'ral_credit_transh_getting_deadline'

        }, inplace=True)

        # df['contract_issue_date'] = df['contract_title'].str.extract(r'(\d{2})\.(\d{2})\.(\d{4})')
        df['credit_agreement_total_volume'] = df['credit_agreement_total_volume'].str.replace(r'\u00A0', '', regex=True)
        df['credit_agreement_total_volume'] = df['credit_agreement_total_volume'].str.replace(r' ', '', regex=True)
        df['credit_agreement_total_volume'] = df['credit_agreement_total_volume'].str.replace(',', '.')
        df['credit_agreement_total_volume'] = df['credit_agreement_total_volume'].astype('float')

        df['credit_volume'] = df['credit_volume'].str.replace(r'\u00A0', '', regex=True)
        df['credit_volume'] = df['credit_volume'].str.replace(r' ', '', regex=True)
        df['credit_volume'] = df['credit_volume'].str.replace(',', '.')
        df['credit_volume'] = df['credit_volume'].astype('float')

        df['credit_tranch_date'] = pd.to_datetime(df['credit_tranch_date'],
                                                  format='%d.%m.%Y %H:%M:%S')  # 11.08.2022 17:26:27
        df = df.copy()
        df['tranch_year'] = df['credit_tranch_date'].dt.year


        df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y %H:%M:%S')
        df['year'] = df['date'].dt.year
        df['quarter'] = df['date'].dt.quarter
        df['month'] = df['date'].dt.month

        df['month_first_date'] = (
                    df['date'].dt.floor('d') + pd.offsets.MonthEnd(0) - pd.offsets.MonthBegin(1))
        df = df.copy()
        df['freelimitremainings'] = df['freelimitremainings'].str.replace(r'\u00A0', '', regex=True)
        df['freelimitremainings'] = df['freelimitremainings'].str.replace(r' ', '', regex=True)
        df['freelimitremainings'] = df['freelimitremainings'].str.replace(',', '.')
        df['freelimitremainings'] = df['freelimitremainings'].replace('', 0)
        df['freelimitremainings'] = df['freelimitremainings'].astype('float')

        df['limitdeadline'] = df['limitdeadline'].replace('', '01.01.2050 0:00:00')
        df['limitdeadline'] = pd.to_datetime(df['limitdeadline'], format='%d.%m.%Y %H:%M:%S')

        df['ral_credit_transh_getting_deadline'] = df['ral_credit_transh_getting_deadline'].replace('', '01.01.2050 0:00:00')
        df['ral_credit_transh_getting_deadline'] = pd.to_datetime(df['ral_credit_transh_getting_deadline'], format='%d.%m.%Y %H:%M:%S')

        df['amount'] = df['amount'].str.replace(r'\u00A0', '', regex=True)
        df['amount'] = df['amount'].str.replace(r' ', '', regex=True)
        df['amount'] = df['amount'].str.replace(',', '.')
        df['amount'] = df['amount'].astype('float')

        df['credit_annual_rate'] = df['credit_annual_rate'].str.replace(r'\u00A0', '', regex=True)
        df['credit_annual_rate'] = df['credit_annual_rate'].str.replace(r' ', '', regex=True)
        df['credit_annual_rate'] = df['credit_annual_rate'].str.replace(',', '.')
        df['credit_annual_rate'] = df['credit_annual_rate'].astype('float')

        df['credit_amount'] = df['credit_volume']
        df['record_datetime'] = datetime.datetime.now()
        url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
        engine = sqlalchemy.create_engine(url_db)



        # создаем таблицу creditDB
        try:
            if_exists = 'replace'
            with engine.connect() as con:
                df.to_sql(
                    name='creditdb_2',
                    con=con,
                    # chunksize=1000,
                    # method='multi',
                    index=False,
                    if_exists=if_exists
                )
        except:
            status_text = "не получилось создать таблицу creditDB"
            status = ''
            return status_text


        # raw_credit_df_head = df.head()
        # data_raw_credit_df_head = raw_credit_df_head.to_dict('records')
        # credit_datatable = dash_table.DataTable(data=data_raw_credit_df_head,)


        # buf = io.StringIO()
        # raw_credit_df_head.info(buf=buf)
        # s = buf.getvalue()

        output_str = html.Div(
            children=[
               html.P("credit table updated")
            ]
        )


        output_mess.append(output_str)

    output_ = output_mess

    return "credit table updated"