import pandas as pd
from pathlib import Path
import sqlalchemy
import os
import random
import sqlite3

def leasing_data_convert_func(reload_leasing_table):
    output = []
    if reload_leasing_table:
        project_folder = Path(__file__).resolve().parent.parent.parent
        leasing_data_convert_file = str(project_folder) + '/leasing_temp_db_2.csv'
        df = pd.read_csv(leasing_data_convert_file, parse_dates=True, low_memory=False)
        df['month_first_date'] = pd.to_datetime(df['month_first_date'])
        df['date'] = pd.to_datetime(df['date'])
        df['record_datetime'] = pd.to_datetime(df['record_datetime'])


        df['customer_name'].fillna("", inplace=True)
        df['company_group'].fillna("", inplace=True)
        df['agreement_type'].fillna("", inplace=True)
        df['current_agreement_status'].fillna("", inplace=True)
        df['leasing_product'].fillna("", inplace=True)
        df['leasing_object_type'].fillna("", inplace=True)
        df['leasing_category_2'].fillna("", inplace=True)
        df['payment_amount'].fillna(0, inplace=True)

        # меняем содержимое в поле customer_name
        # ищем пустые строки и заполняем их
        df['customer_name_temp'] = df['customer_name']
        df['customer_name_temp'].fillna("test", inplace=True)
        df['customer_name_temp'] = df['customer_name_temp'].replace('', 'test', regex=True)

        df_temp = df.loc[df['customer_name_temp'] != "test"]

        df['payment_amount'] = df['payment_amount'] / 8

        list_of_customer_name = list(df_temp['customer_name'].unique())
        result_df_list = []
        address_file = str(project_folder) + '/address.csv'
        addresses_df = pd.read_csv(address_file)

        addresses_df = addresses_df.reset_index()
        addresses_df = addresses_df.rename(columns={"index": "address_id"})
        number_of_rows = len(addresses_df)
        # output.append(f'number_of rows: {number_of_rows}')

        # создаем таблицу в которой у одного клиента - одна точка с координатами
        addresses_df['customer_name'] = "Контрагент № " + addresses_df['address_id'].astype(str)

        addresses_df.rename(columns={
            'geo_lat': 'latitude',
            'geo_lon': 'longitude'
        }, inplace=True)


        try:
            if_exists = 'replace'
            url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
            engine = sqlalchemy.create_engine(url_db)

            with engine.connect() as con:
                addresses_df.to_sql(
                    name='customer_address',
                    con=con,
                    chunksize=5000,
                    method='multi',
                    index=False,
                    if_exists=if_exists
                )
            output.append('customer_product_category updated')
        except Exception as e:
            output.append(f"не получилось создать таблицу customer_product_category: {e}")

            return str(output)






        # создаем таблицу по клиентам с категорией продукции, которую они покупают
        product_category_list = [
            'Канцелярские товары',
            'Продукты питания',
            'Велосипеды',
            'Запасные части для швейных машин',
            'Уменьшители хода',
            'Шины и диски',
            'Электрические удлинители',
            'Роботы-пылесосы',
        ]
        customer_product_category_list = []
        # итерируемся по группам продуктов
        for product_group in product_category_list:
            # берем семпл из клиентов
            total_df_customers_rows = len(addresses_df)
            sample_qty = int(round(total_df_customers_rows / 5, 0))
            customer_sample_df = addresses_df.sample(n=sample_qty)
            # список клиентов в выборке
            sample_customer_list = list(customer_sample_df['customer_name'].unique())
            for customer in sample_customer_list:
                temp_dict = {}
                temp_dict['customer_name'] = customer
                temp_dict['product_category'] = product_group
                customer_product_category_list.append(temp_dict)

        customer_product_category_df = pd.DataFrame(customer_product_category_list)

        # print(customer_product_category_df)




        #############################  ПЕРЕИМЕНОВАНИЕ КЛИЕНТОВ ########################
        rename_dict = {}
        list_of_customer_name = list(df_temp['customer_name_temp'].unique())
        i = 1
        for item in list_of_customer_name:
            new_name = f'Контрагент № {i}'
            rename_dict[item] = new_name
            i = i + 1

        df['customer_name_temp'] = df['customer_name'].map(rename_dict)

        list_of_customer_name = list(df['customer_name_temp'].unique())

        df.pop('customer_name')
        df.rename(columns={
            'customer_name_temp': 'customer_name'
        }, inplace=True)

        #########################################################################################



        for customer in list_of_customer_name:
            temp_dict = {}
            sample_address_df = addresses_df.sample(n=1)
            longitude = sample_address_df.iloc[0]['longitude']
            latitude = sample_address_df.iloc[0]['latitude']
            address_id = sample_address_df.iloc[0]['address_id']

            # longitude = random.uniform(30, 103) # по горизонтали
            # latitude = random.uniform(52, 61) # по вертикали
            temp_dict['customer_name'] = customer
            temp_dict['latitude'] = latitude
            temp_dict['longitude'] = longitude
            temp_dict['address_id'] = address_id


            result_df_list.append(temp_dict)
        df_customers = pd.DataFrame(result_df_list)





        try:
            if_exists = 'replace'
            url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
            engine = sqlalchemy.create_engine(url_db)

            with engine.connect() as con:
                customer_product_category_df.to_sql(
                    name='customer_product_category',
                    con=con,
                    chunksize=5000,
                    method='multi',
                    index=False,
                    if_exists=if_exists
                )
            output.append('customer_product_category updated')
        except Exception as e:
            output.append(f"не получилось создать таблицу customer_product_category: {e}")

            return str(output)



        # меняем содержимое в поле company_group
        # ищем пустые строки и заполняем их
        df['company_group_temp'] = df['company_group']
        df['company_group_temp'].fillna("test", inplace=True)
        df['company_group_temp'] = df['company_group_temp'].replace('', 'test', regex=True)

        df_temp = df.loc[df['company_group_temp'] != "test"]

        rename_dict = {}
        list_of_customer_name = list(df_temp['company_group_temp'].unique())
        i = 1
        for item in list_of_customer_name:
            new_name = f'Холдинг № {i}'
            rename_dict[item] = new_name
            i = i + 1

        df['company_group_temp'] = df['company_group'].map(rename_dict)
        df.pop('company_group')
        df.rename(columns={
            'company_group_temp': 'company_group'
        }, inplace=True)



        try:
            if_exists = 'replace'
            # url_db = 'postgresql+psycopg2://postgres:123456@db:5432/postgres'
            url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
            engine = sqlalchemy.create_engine(url_db)

            with engine.connect() as con:
                df_customers.to_sql(
                    name='customers',
                    con=con,
                    chunksize=5000,
                    method='multi',
                    index=False,
                    if_exists=if_exists
                )
            output.append('df_coordiates updated')
        except Exception as e:
            output.append(f"не получилось создать таблицу df_coordiates: {e}")

            return str(output)


        try:
            if_exists = 'replace'
            # url_db = 'postgresql+psycopg2://postgres:123456@db:5432/postgres'
            url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
            engine = sqlalchemy.create_engine(url_db)

            with engine.connect() as con:
                df.to_sql(
                    name='leasing_temp_db',
                    con=con,
                    chunksize=5000,
                    method='multi',
                    index=False,
                    if_exists=if_exists
                )
            output.append('leasing_temp_db updated')
        except Exception as e:
            output.append(f"не получилось создать таблицу leasing_temp_db: {e}")

            return str(output)


        return str(output)
    return str(output)




# leasing_data_convert_func(1)