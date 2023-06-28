import json
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
from pathlib import Path
import os
import sqlalchemy
import xmltodict
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from dash import dash_table
import io
def leasing_data_to_bd_func():
    url = "http://ral-61.rosagroleasing.ru/work1cbuh_2_0/ws/GetDataFromReports.1cws"
    user = "UserGetDataFromReports"
    password = "Q!cmo7djz41rto"

    headers = {'content-type': 'text/xml'}
    list_of_years = [2023, 2024, 2025, 2026, 2027, 2028, 2029]
    # list_of_years = [2023]
    records_number = 0
    url_db = os.environ["SQLALCHEMY_DATABASE_URI"]
    engine = sqlalchemy.create_engine(url_db)
    try:
        def drop_table(table_name, engine=engine):
            Base = declarative_base()
            metadata = MetaData()
            metadata.reflect(bind=engine)
            table = metadata.tables[table_name]
            if table is not None:
                Base.metadata.drop_all(engine, [table], checkfirst=True)

        drop_table('leasingdb_3')
    except:
        return "не получилось дропнуть таблицу"
    raw_df_columns = ""
    for year in list_of_years:
        body_leasing_request = f"""
                        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:uri="uri.rosagroleasing.ru:GetDataFromReports">
    
                           <soapenv:Header/>
    
                           <soapenv:Body>
    
                              <uri:ДоговораЛизингаСводныеДанныеГДАППоМесяцам>
    
                                 <uri:ДатаНачала>{str(year)}-01-01</uri:ДатаНачала>
    
    
                                 <uri:ДатаОкончания>{str(year+1)}-01-01</uri:ДатаОкончания>
    
                              </uri:ДоговораЛизингаСводныеДанныеГДАППоМесяцам>
    
                           </soapenv:Body>
    
                        </soapenv:Envelope>
                        """
        body_leasing_request = body_leasing_request.encode('utf-8')
        response_leasing_request = requests.post(url, data=body_leasing_request, headers=headers,
                                                 auth=HTTPBasicAuth(user, password))

        response_leasing_request_dict_data = xmltodict.parse(response_leasing_request.content.decode('utf-8'))
        data_leasing_raw_data = response_leasing_request_dict_data['soap:Envelope']['soap:Body'][
            'm:ДоговораЛизингаСводныеДанныеГДАППоМесяцамResponse'][
            'm:return']['#text']


        try:
            # на входе я получаю строку. Поэтому для начала мы ее парсим в json - а на самом деле в дикт
            data_leasing_raw_data = json.loads(data_leasing_raw_data)
            # data_leasing_raw_data_dict_type = str(type(data_leasing_raw_data_dict))

            # data_leasing_raw_data = data_leasing_raw_data[0]
            raw_df = pd.DataFrame.from_records(data_leasing_raw_data)
            raw_df_columns = str(raw_df.columns)
            raw_df.rename(columns={
                'ДатаГрафика': 'date',
                'ГруппаКомпаний': 'company_group',
                'Контрагент': 'customer_name',
                'Д_СтатусТекущий': 'current_agreement_status',
                'ГДАП_АрендныйПлатежСНДС': 'payment_amount'

            }, inplace=True)
            df = raw_df
            df['payment_amount'] = df['payment_amount'].str.replace(r'\u00A0', '', regex=True)
            df['payment_amount'] = df['payment_amount'].str.replace(r' ', '', regex=True)
            df['payment_amount'] = df['payment_amount'].str.replace(',', '.')
            df['payment_amount'] = df['payment_amount'].astype('float')
            df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y %H:%M:%S')
            df['year'] = df['date'].dt.year
            df['month'] = df['date'].dt.month
            df = df.loc[:, ['date', 'month', 'year', 'company_group','customer_name', 'current_agreement_status', 'payment_amount']]

            records_number = records_number + len(df)
            if_exists = 'append'
            with engine.connect() as con:
                df.to_sql(
                    name='leasingdb_3',
                    con=con,
                    # chunksize=1000,
                    # method='multi',
                    # index=False,
                    if_exists=if_exists
                )
        except Exception as e:
            return f"conversion error {e}"

    return f'кол-во записей: {str(records_number)}'

        # df.to_sql('leasingDB', con=engine, if_exists='replace')

        # temp_df = df.head(100)
        # data = temp_df.to_dict('records')
        # credit_datatable = dash_table.DataTable(data=data)
        # return credit_datatable

        # data_leasing = str(data_leasing_raw_data)
        # data_2 = data_leasing.replace('"', "'")
        # data_3 = data_2.replace("'", '"')
        # data_4 = data_3.replace('\\"', "")
        # data_5 = data_4.replace('\\xa0', '')
        # data_json = json.loads(data_5)
        # df = pd.DataFrame(data_json)
        # df.rename(columns={
        #     'ДатаГрафика': 'date',
        #     'Д_СтатусТекущий': 'current_agreement_status',
        #     'ГДАП_АрендныйПлатежСНДС': 'payment_amount'
        #
        # }, inplace=True)
        #
        # df['payment_amount'] = df['payment_amount'].str.replace(r'\u00A0', '', regex=True)
        # df['payment_amount'] = df['payment_amount'].str.replace(r' ', '', regex=True)
        # df['payment_amount'] = df['payment_amount'].str.replace(',', '.')
        # df['payment_amount'] = df['payment_amount'].astype('float')
        #
        # df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y %H:%M:%S')
        # df['year'] = df['date'].dt.year
        # df['month'] = df['date'].dt.month
        # df = df.loc[:, ['date', 'month', 'year', 'current_agreement_status', 'payment_amount']]
        # project_folder = Path(__file__).resolve().parent.parent.parent
        # # db_dir = str(project_folder) + '/database'
        # # url = 'sqlite:///' + os.path.join(db_dir, 'datab.db')



    #     return f"data ok {str(df)}"
    # except Exception as e:
    #     return f"data not ok {e}"