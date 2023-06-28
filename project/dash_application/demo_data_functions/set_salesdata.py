import datetime
import os
from sqlalchemy import create_engine
import pandas as pd
import random
import numpy as np
from dash import dash_table
import datetime
def set_salesdata_func():
    output  = 'test'

    # получаем таблицу leasing_temp_db
    url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
    engine = create_engine(url_db, pool_recycle=3600)
    with engine.connect() as con:
        query = 'SELECT *  FROM "leasing_temp_db";'
        df_leasing_temp_db = pd.read_sql(query, con)

    df = df_leasing_temp_db.loc[:, ['customer_name', 'payment_amount', 'date']]

    df['customer_name'].fillna("test", inplace=True)
    df['customer_name'] = df['customer_name'].replace('', 'test', regex=True)

    df = df.loc[df['customer_name'] != "test"]
    df.sort_values(['date'], inplace=True)

    with engine.connect() as con:
        query = 'SELECT *  FROM "customer_product_category";'
        df_customers_product_categories = pd.read_sql(query, con)

    # список продуктовых категорий:
    product_categories_list = list(df_customers_product_categories['product_category'].unique())

    customer_name_list = list(df['customer_name'].unique())

    payment_amount_list = list(df['payment_amount'].unique())

    # random_category = random.choice(product_categories_list)



    result_df = []

    # заполняем данные с начала 2023 года данными мая июня июля

    start_date = datetime.datetime(2023, 4,1)
    finish_date = datetime.datetime(2023, 6, 1)
    df.sort_values(['date'], inplace = True)

    for row in df.itertuples():
        temp_dict = {}
        current_date = getattr(row, 'date')
        current_date_year = current_date.year
        current_date_month = current_date.month
        current_date_day = current_date.day
        new_month = 1
        try:
            new_month = current_date_month - 3
        except:
            pass
        try:
            new_datetime = datetime.datetime(current_date_year, new_month, current_date_day)

            temp_dict['date'] = new_datetime

            customer_name = getattr(row, 'customer_name')
            temp_dict['customer_name'] = customer_name

            payment_amount = getattr(row, 'payment_amount')
            temp_dict['payment_amount'] = payment_amount

            result_df.append(temp_dict)
            if new_datetime >= datetime.datetime(2023, 4, 5):
                break
        except:
            pass



    jan_apr_data_df = pd.DataFrame(result_df)

    df = pd.concat([jan_apr_data_df, df])

    df['product_category'] = np.random.choice(product_categories_list, df.shape[0])

    # получаем продажи в текущем календарном году
    today_datetime = datetime.datetime.now()
    current_year = today_datetime.year

    start_datetime_current_year = datetime.datetime(current_year, 1,1)

    df_sales_current_year = df.loc[df['date']>=start_datetime_current_year]
    # df_sales_current_year = df_sales_current_year.loc[df_sales_current_year['date']<=today_datetime]
    df_sales_current_year.sort_values(['date'], inplace=True)

    # получаем таблицу с каждфм днем в году
    first_day = datetime.datetime(current_year,1,1)
    last_day = datetime.datetime(current_year, 12, 31)

    temp_date = first_day

    list_df = []
    while temp_date <= last_day:
        temp_dict = {}
        temp_dict['datetime'] = temp_date
        temp_date = temp_date + datetime.timedelta(days=1)
        list_df.append(temp_dict)

    calendar_df = pd.DataFrame(list_df)

    # итерируемся по calendar_df
    list_of_dates  = list(calendar_df['datetime'].unique())

    list_df = []
    for calendar_datetime in list_of_dates:
        # итерируемся по продуктовым группам
        for product_category in product_categories_list:
            temp_dict = {}
            # режем df_sales_current_year
            temp_category_calendar_df = df_sales_current_year.loc[df_sales_current_year['date']==calendar_datetime]
            temp_category_calendar_df = temp_category_calendar_df.loc[temp_category_calendar_df['product_category']==product_category]
            if len(temp_category_calendar_df)>0:
                payment_amount = temp_category_calendar_df.iloc[0]['payment_amount']
            else:
                payment_amount = 0

            temp_dict['date'] = calendar_datetime
            temp_dict['product_category'] = product_category
            temp_dict['payment_amount'] = payment_amount
            calendar_datetime = pd.to_datetime(calendar_datetime)
            temp_dict['quarter'] = (calendar_datetime.month-1)//3+1

            list_df.append(temp_dict)

    calendar_sales_df_v2 = pd.DataFrame(list_df)


    ########### ПЛАНЫ
    list_df = []
    for row in calendar_sales_df_v2.itertuples():
        temp_dict = {}
        temp_dict['date'] = getattr(row, 'date')
        product_category = getattr(row, 'product_category')
        temp_dict['product_category'] = product_category
        quarter = getattr(row, 'quarter')
        temp_dict['quarter'] = quarter
        temp_dict['payment_amount'] = getattr(row, 'payment_amount')

        temp_df = calendar_sales_df_v2.loc[calendar_sales_df_v2['product_category']==product_category]
        temp_df = temp_df.loc[temp_df['quarter']==quarter]
        product_category_payment_amount = temp_df['payment_amount'].sum()


        plan_value = product_category_payment_amount * 1.1
        temp_dict['plan'] =plan_value
        list_df.append(temp_dict)

    calendar_sales_v3 = pd.DataFrame(list_df)

    url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
    engine = create_engine(url_db, pool_recycle=3600)
    with engine.connect() as con:
        calendar_sales_v3.to_sql(
            name='calendar_sales_v3',
            con=con,
            chunksize=5000,
            method='multi',
            index=False,
            if_exists="replace"
        )






    url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
    engine = create_engine(url_db, pool_recycle=3600)
    with engine.connect() as con:
        calendar_sales_df_v2.to_sql(
            name='calendar_sales_v2',
            con=con,
            chunksize=5000,
            method='multi',
            index=False,
            if_exists="replace"
        )




    calendar_sales_df = calendar_df.merge(df_sales_current_year, left_on='datetime', right_on='date', how='left')
    calendar_sales_df['quarter'] = calendar_sales_df['date'].dt.quarter

    url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
    engine = create_engine(url_db, pool_recycle=3600)
    with engine.connect() as con:
        calendar_sales_df.to_sql(
            name='calendar_sales',
            con=con,
            chunksize=5000,
            method='multi',
            index=False,
            if_exists="replace"
        )


    url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
    engine = create_engine(url_db, pool_recycle=3600)
    with engine.connect() as con:
        df_sales_current_year.to_sql(
            name='sales_current_year',
            con=con,
            chunksize=5000,
            method='multi',
            index=False,
            if_exists="replace"
        )


    # datatable = dash_table.DataTable(data=df_sales_current_year.to_dict('records'), )
    output = ""


    return output
