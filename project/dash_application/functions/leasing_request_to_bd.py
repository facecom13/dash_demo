import datetime
import time
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
import psycopg2

def leasing_request_to_bd_func(data_input):
    status_text = ''
    status = []
    if data_input == '1с_api':
        url = "http://ral-61.rosagroleasing.ru/work1cbuh_2_0/ws/GetDataFromReports.1cws"
        user = "UserGetDataFromReports"
        password = "Q!cmo7djz41rto"

        headers = {'content-type': 'text/xml'}
        list_of_years = [2023, 2024, 2025, 2026, 2027, 2028, 2029,2030, 2031, 2032, 2033, 2034, 2035, 2036, 2037, 2038, 2039, 2040]
        # list_of_years = [2023]
        month_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        # month_list = [1]
        now_start = datetime.datetime.now()
        status.append(str(now_start))
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

            drop_table('leasing_temp_db_2')
        except:
            # return "не получилось дропнуть таблицу"
            pass

        for year in list_of_years:
            month_calendar = {
                1: {"start_date": f"{str(year)}-01-01", "finish_date": f"{str(year)}-01-31"},
                2: {"start_date": f"{str(year)}-02-01", "finish_date": f"{str(year)}-02-28"},
                3: {"start_date": f"{str(year)}-03-01", "finish_date": f"{str(year)}-03-31"},
                4: {"start_date": f"{str(year)}-04-01", "finish_date": f"{str(year)}-04-30"},
                5: {"start_date": f"{str(year)}-05-01", "finish_date": f"{str(year)}-05-31"},
                6: {"start_date": f"{str(year)}-06-01", "finish_date": f"{str(year)}-06-30"},
                7: {"start_date": f"{str(year)}-07-01", "finish_date": f"{str(year)}-07-31"},
                8: {"start_date": f"{str(year)}-08-01", "finish_date": f"{str(year)}-08-31"},
                9: {"start_date": f"{str(year)}-09-01", "finish_date": f"{str(year)}-09-30"},
                10: {"start_date": f"{str(year)}-10-01", "finish_date": f"{str(year)}-10-31"},
                11: {"start_date": f"{str(year)}-11-01", "finish_date": f"{str(year)}-11-30"},
                12: {"start_date": f"{str(year)}-12-01", "finish_date": f"{str(year)}-12-31"},

            }
            for month_number in month_list:
                time.sleep(5)

                start_date = month_calendar[month_number]["start_date"]
                finish_date = month_calendar[month_number]["finish_date"]
                # start_date = f"{str(year)}-01-01"
                # finish_date =f"{str(year)}-12-31"

                body_leasing_request = f"""
                                        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:uri="uri.rosagroleasing.ru:GetDataFromReports">
    
                                           <soapenv:Header/>
    
                                           <soapenv:Body>
    
                                              <uri:ДоговораЛизингаСводныеДанныеГДАППоМесяцам>
    
                                                 <uri:ДатаНачала>{start_date}</uri:ДатаНачала>
    
    
                                                 <uri:ДатаОкончания>{finish_date}</uri:ДатаОкончания>
    
                                              </uri:ДоговораЛизингаСводныеДанныеГДАППоМесяцам>
    
                                           </soapenv:Body>
    
                                        </soapenv:Envelope>
                                        """
                body_leasing_request = body_leasing_request.encode('utf-8')
                leasing_response = ''
                try:
                    leasing_response = requests.post(url, data=body_leasing_request, headers=headers,
                                                     auth=HTTPBasicAuth(user, password))

                    status.append(str(leasing_response))
                    leasing_response.raise_for_status()
                except requests.exceptions.HTTPError as err:
                    # raise SystemExit(err)
                    status.append(str(SystemExit(err)))
                except Exception as e:
                    status.append(e)


                    # if "200" not in str(leasing_response):
                    #     status.append(f"получен ответ {str(leasing_response)} на year: {str(year)} month: {str(month_number)}")
                    #     return str(status)

                # except Exception as leasing_request_error:
                #     status_text = "Не удалось получить данные uri:ДоговораЛизингаСводныеДанныеГДАППоМесяцам"
                #     status.append('failed_leasing_request')
                #     return status

                dict_data = xmltodict.parse(leasing_response.content.decode('utf-8'))

                data_leasing_dict = \
                dict_data['soap:Envelope']['soap:Body']['m:ДоговораЛизингаСводныеДанныеГДАППоМесяцамResponse'][
                    'm:return']['#text']
                # записываем данные в БД
                data_leasing_raw_data = json.loads(data_leasing_dict)
                raw_leasing_df = pd.DataFrame.from_records(data_leasing_raw_data)
                df = raw_leasing_df
                df.rename(columns={
                    'Контрагент': 'customer_name',
                    'ГруппаКомпаний': 'company_group',
                    'ДатаГрафика': 'date',
                    'Д_СтатусТекущий': 'current_agreement_status',
                    'Д_ВидДоговораУпрУчета': 'agreement_type',
                    'Д_ЛизинговыйПродукт': 'leasing_product',
                    'ДоходЛК': 'leasing_rate',
                    'Д_ВидПредметаЛизинга': 'leasing_object_type',
                    'Д_ВидВзаиморасчетов': 'leasing_category_2',

                    'ГДАП_АрендныйПлатежСНДС': 'payment_amount'

                }, inplace=True)

                df['payment_amount'] = df['payment_amount'].str.replace(r'\u00A0', '', regex=True)
                df['payment_amount'] = df['payment_amount'].str.replace(r' ', '', regex=True)
                df['payment_amount'] = df['payment_amount'].str.replace(',', '.')
                df['payment_amount'] = df['payment_amount'].astype('float')

                df['leasing_rate'] = df['leasing_rate'].str.replace(r'\u00A0', '', regex=True)
                df['leasing_rate'] = df['leasing_rate'].str.replace(r' ', '', regex=True)
                df['leasing_rate'] = df['leasing_rate'].str.replace(',', '.')
                df['leasing_rate'] = df['leasing_rate'].astype('float')


                df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y %H:%M:%S')
                df['year'] = df['date'].dt.year
                df['month'] = df['date'].dt.month
                df['record_datetime'] = datetime.datetime.now()
                df['month_first_date'] = (
                        df['date'].dt.floor('d') + pd.offsets.MonthEnd(0) - pd.offsets.MonthBegin(1))


                url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
                engine = sqlalchemy.create_engine(url_db)
                # создаем таблицу leasingDB
                try:
                    if_exists = 'append'
                    with engine.connect() as con:
                        df.to_sql(
                            name="leasing_temp_db_2",
                            con=con,
                            # chunksize=1000,
                            # method='multi',
                            index=False,
                            if_exists=if_exists
                        )
                except Exception as e_create_leasing_table:
                    status_text = f"не получилось создать таблицу leasingDB {e_create_leasing_table}"
                    status.append(f"не получилось создать таблицу leasingDB {e_create_leasing_table}")
                    return str(status)

            ################################## ЗАВЕРШЕНИЕ ЦИКЛА #####################################


        ################################# готовим таблицу по 'Д_ЛизинговыйПродукт': 'leasing_product ##############################



        #####################################################################################################


        status_text = f"leasingDB updated"

        status.append('leasing tables updated')
        now = datetime.datetime.now()
        status.append(str(now))

    return str(status)