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
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
def credit_request_to_bd_func(data_input):
    status_text = ''
    status = 'ok'
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

                            <uri:ДатаОкончания>2034-01-01</uri:ДатаОкончания>

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
            return status_text, status

        dict_data = xmltodict.parse(credit_response.content.decode('utf-8'))
        data_credit = \
            dict_data['soap:Envelope']['soap:Body']['m:ГрафикиПогашенияКредитовИОблигацийВСтрочкуResponse'][
                'm:return']['#text']

        data_credit_raw_data = json.loads(data_credit)
        raw_credit_df = pd.DataFrame.from_records(data_credit_raw_data)
        df = raw_credit_df
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
            'Ставка': 'credit_annual_rate'

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
        df['tranch_year'] = df['credit_tranch_date'].dt.year

        df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y %H:%M:%S')
        df['year'] = df['date'].dt.year
        df['quarter'] = df['date'].dt.quarter
        df['month_first_date'] = (
                    df['date'].dt.floor('d') + pd.offsets.MonthEnd(0) - pd.offsets.MonthBegin(1))

        df['amount'] = df['amount'].str.replace(r'\u00A0', '', regex=True)
        df['amount'] = df['amount'].str.replace(r' ', '', regex=True)
        df['amount'] = df['amount'].str.replace(',', '.')
        df['amount'] = df['amount'].astype('float')

        df['credit_annual_rate'] = df['credit_annual_rate'].str.replace(r'\u00A0', '', regex=True)
        df['credit_annual_rate'] = df['credit_annual_rate'].str.replace(r' ', '', regex=True)
        df['credit_annual_rate'] = df['credit_annual_rate'].str.replace(',', '.')
        df['credit_annual_rate'] = df['credit_annual_rate'].astype('float')

        df['credit_amount'] = df['credit_volume']
        df['datetime'] = datetime.datetime.now

        url_db = os.environ["SQLALCHEMY_DATABASE_URI"]
        engine = sqlalchemy.create_engine(url_db)

        # создаем таблицу creditDB
        try:
            if_exists = 'replace'
            with engine.connect() as con:
                df.to_sql(
                    name='creditDB',
                    con=con,
                    # chunksize=1000,
                    # method='multi',
                    index=False,
                    if_exists=if_exists
                )
        except:
            status_text = "не получилось создать таблицу creditDB"
            status = ''
            return status_text, status


        raw_credit_df_head = df.head()
        data_raw_credit_df_head = raw_credit_df_head.to_dict('records')
        credit_datatable = dash_table.DataTable(data=data_raw_credit_df_head,)


        buf = io.StringIO()
        raw_credit_df_head.info(buf=buf)
        s = buf.getvalue()

        output_str = html.Div(
            children=[
               html.P("credit table updated")
            ]
        )


        status_text = output_str

    return status_text

if __name__ == "__main__":
    print(f"Running script at {datetime.datetime.now()}")
    credit_request_to_bd_func('1с_api')
