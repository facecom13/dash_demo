import pandas as pd
import os
import sqlalchemy
from sqlalchemy import create_engine
import psycopg2
def leasing_short_table_create_func(data_input):
    output = ''
    if data_input =='1с_api':
        # output = 'test_create_leasing_tables_output_div_content'
        url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
        engine = create_engine(url_db, pool_recycle=3600)

        with engine.connect() as con:
            # query = 'SELECT customer_name, company_group, year, month, current_agreement_status,month_first_date, SUM(payment_amount)  FROM "leasingDB" GROUP BY customer_name, company_group, year, month, current_agreement_status,month_first_date;'
            query = 'SELECT customer_name, company_group, year, month, current_agreement_status,month_first_date, SUM(payment_amount)  FROM "leasing_temp_DB" GROUP BY customer_name, company_group, year, month, current_agreement_status,month_first_date;'
            df = pd.read_sql(query, con)
            df[['customer_name', 'company_group', 'current_agreement_status']].apply(lambda x: x.astype('category'))
            df['month_first_date'] = pd.to_datetime(df['month_first_date'])
            # удаляем строки, в которых нет статуса
            df['current_agreement_status'].fillna('delete', inplace=True)
            df = df.loc[~df['current_agreement_status'].isin(['delete', ''])]
            # удаляем строки, в которых нет клиента
            df['customer_name'].fillna('delete', inplace=True)
            df = df.loc[~df['customer_name'].isin(['delete', ''])]

            df['year'] = df['year'].astype('int32')
            df['month'] = df['month'].astype('int32')
            df.rename(columns={
                'sum': 'payment_amount'
            }, inplace=True)

        return df

        # output = "Кол-во строк: " + str(len(df))

    return output


# engine = create_engine('postgresql+psycopg2://postgres:123456@db:5432/dash_db', pool_recycle=3600)
        # df = pd.read_sql_query('select * from "leasingDB";', con=engine)


# cur = conn.cursor()
# df.to_sql(
            #     name='leasingDB',
            #     con=con,
            #     # chunksize=1000,
            #     # method='multi',
            #     # index=False,
            #     i