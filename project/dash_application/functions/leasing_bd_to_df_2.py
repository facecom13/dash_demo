import sqlite3
import os
import pandas as pd
from sqlalchemy import create_engine

def leasing_bd_to_df_2_func(data_input):
    if data_input == 'demo':

        SQLITE_URL = os.environ["SQLITE_URL"]

        conn = sqlite3.connect(SQLITE_URL)
        cur = conn.cursor()
        query = 'SELECT * FROM "leasingdemoDB";'
        df = pd.read_sql(query, conn)



        df.sort_values(by="date", inplace=True)

        # df['credit_tranch_date'] = pd.to_datetime(df['credit_tranch_date'], format='%d.%m.%Y %H:%M:%S')
        df['date'] = pd.to_datetime(df['date'])

        df['month_first_date'] = (df['date'].dt.floor('d') + pd.offsets.MonthEnd(0) - pd.offsets.MonthBegin(1))
        # print(df.info())
        df_groupped = df.groupby(['month_first_date','month', 'year','company_group', 'customer_name', 'current_agreement_status'], as_index=False).agg(
            {'payment_amount': 'sum'})
        cur.close()
        conn.close()

        return df_groupped

    elif data_input == '1с_api':
        # Получаем данные из базы
        url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
        engine = create_engine(url_db, pool_recycle=3600)
        df = pd.read_sql_query('select * from "leasingDB";', con=engine)
        try:
            df['date'] = pd.to_datetime(df['date'])
        except:
            pass

        try:
            df['month_first_date'] = (df['date'].dt.floor('d') + pd.offsets.MonthEnd(0) - pd.offsets.MonthBegin(1))
        except:
            pass
        # удаляем строки, в которых нет статуса
        df['current_agreement_status'].fillna('delete', inplace=True)
        df = df.loc[~df['current_agreement_status'].isin(['delete', ''])]
        # удаляем строки, в которых нет клиента
        df['customer_name'].fillna('delete', inplace=True)
        df = df.loc[~df['customer_name'].isin(['delete', ''])]


        df['payment_amount'] = df['payment_amount'].astype(float)

        df_groupped = df.groupby(['month_first_date','year','month', 'customer_name','company_group', 'current_agreement_status'], as_index=False).agg({'payment_amount': 'sum'})

        return df_groupped