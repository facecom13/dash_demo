import json
import pandas as pd
from extensions import extensions
import sqlalchemy
import os

from sqlalchemy import create_engine

import dash_application.functions.leasing_data as leasing_data

db = extensions.db

def record_leasing_raw_data_to_database_func(data_leasing_dict, data_input):
    data_credit = str(data_leasing_dict)
    data_2 = data_credit.replace('"', "'")
    data_3 = data_2.replace("'", '"')
    data_4 = data_3.replace('\\"', "")
    data_5 = data_4.replace('\\xa0', '')
    data_6 = data_5.replace('\\n', '')
    # print("data_6: ", data_6)
    data_json = json.loads(data_6)
    df = pd.DataFrame(data_json)
    df.rename(columns={
        'ДатаГрафика': 'date',
        'Д_СтатусТекущий': 'current_agreement_status',
        'ГДАП_АрендныйПлатежСНДС': 'payment_amount'

    }, inplace=True)

    df['payment_amount'] = df['payment_amount'].str.replace(r'\u00A0', '', regex=True)
    df['payment_amount'] = df['payment_amount'].str.replace(r' ', '', regex=True)
    df['payment_amount'] = df['payment_amount'].str.replace(',', '.')
    df['payment_amount'] = df['payment_amount'].astype('float')

    df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y %H:%M:%S')
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df = df.loc[:, ['date', 'month', 'year', 'current_agreement_status', 'payment_amount']]

    db_uri = os.environ.get('SQLALCHEMY_DATABASE_URI')
    engine = create_engine(db_uri)
    # Write data into the table in sqllite database
    # LeasingdataDB.__table__.drop(engine)

    # df.to_sql('leasingdataDB', engine)
    # try:
    #     leasingdatademoDB.__table__.drop(engine)
    # except:
    #     pass
    # if data_input == 'demo':
    #     try:
    #         leasingdatademoDB.__table__.drop(engine)
    #     except:
    #         pass
    #     try:
    #         df.to_sql('leasingdatademoDB', engine)
    #     except:
    #         pass

    # elif data_input == '1c_api':
    #     # try:
    #     leasingdatademoDB.__table__.drop(engine)
        # except:
        #     pass
        # try:
        #     df.to_sql('leasingdatademoDB', engine, index=False)
        # except:
        #     pass



    bd_record_output = "data_bd_ok"

    return bd_record_output