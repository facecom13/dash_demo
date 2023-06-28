import pandas as pd
import os
import sqlalchemy
from sqlalchemy import create_engine
import psycopg2

def leasing_tables_create_func(data_input):
    output = []
    if data_input =='1с_api':
        # output = 'test_create_leasing_tables_output_div_content'
        url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
        engine = create_engine(url_db, pool_recycle=3600)


        ############################### СОЗДАНИЕ ТАБЛИЦЫ ДЛЯ ГРАФИКА ПО СТАТУСАМ ДОГОВОРОВ ДЛЯ ВРЕМЕННОГО ГРАФИКА ##########
        # готовим таблицу по 'Д_СтатусТекущий': 'current_agreement_status'
        with engine.connect() as con:

            query = 'SELECT current_agreement_status, year, month, month_first_date, SUM(payment_amount)  FROM "leasing_temp_DB" GROUP BY current_agreement_status, year, month ,month_first_date;'
            df = pd.read_sql(query, con)
            df[['current_agreement_status']].apply(lambda x: x.astype('category'))
            df['month_first_date'] = pd.to_datetime(df['month_first_date'])
            # удаляем строки, в которых нет current_agreement_status
            df['current_agreement_status'].fillna('delete', inplace=True)
            df = df.loc[~df['current_agreement_status'].isin(['delete', ''])]

            df['year'] = df['year'].astype('int32')
            df['month'] = df['month'].astype('int32')
            df.rename(columns={
                'sum': 'payment_amount'
            }, inplace=True)

            # удаляем ненужные статусы
            full_agreement_status_list = list(df['current_agreement_status'].unique())
            # оставляем только нужные статусы договоров
            updated_full_agreement_status_list = []
            for agreement_status in full_agreement_status_list:
                if 'действует' in agreement_status.lower() or 'подписан' in agreement_status.lower():
                    updated_full_agreement_status_list.append(agreement_status)

            updated_status_df = df.loc[df['current_agreement_status'].isin(updated_full_agreement_status_list)]

            df = updated_status_df
            df_temp = df.groupby(['current_agreement_status', 'year', 'month', 'month_first_date'], as_index=False).agg(
                {'payment_amount': 'sum'})
            df = df_temp

        url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
        engine = sqlalchemy.create_engine(url_db)
        # создаем таблицу current_agreement_status
        try:
            if_exists = 'replace'
            with engine.connect() as con:
                df.to_sql(
                    name="current_agreement_status",
                    con=con,
                    # chunksize=1000,
                    # method='multi',
                    index=False,
                    if_exists=if_exists
                )
            output.append('таблица current_agreement_status создана')
        except Exception as e:
            output.append(f'таблица current_agreement_status не создана {e}')

        ##############################################################################################

        ############################### СОЗДАНИЕ ТАБЛИЦЫ ДЛЯ ГРАФИКА ПО agreement_type##########
        # готовим таблицу по 'Д_ВидДоговораУпрУчета': 'agreement_type
        with engine.connect() as con:

            query = 'SELECT current_agreement_status, agreement_type, year, month, month_first_date, SUM(payment_amount)  FROM "leasing_temp_DB" GROUP BY current_agreement_status, agreement_type, year, month ,month_first_date;'
            df = pd.read_sql(query, con)
            df[['agreement_type']].apply(lambda x: x.astype('category'))
            df['month_first_date'] = pd.to_datetime(df['month_first_date'])
            # удаляем строки, в которых нет agreement_type
            df['agreement_type'].fillna('delete', inplace=True)
            df = df.loc[~df['agreement_type'].isin(['delete', ''])]

            df['year'] = df['year'].astype('int32')
            df['month'] = df['month'].astype('int32')
            df.rename(columns={
                'sum': 'payment_amount'
            }, inplace=True)

            # удаляем ненужные статусы
            full_agreement_status_list = list(df['current_agreement_status'].unique())
            # оставляем только нужные статусы договоров
            updated_full_agreement_status_list = []
            for agreement_status in full_agreement_status_list:
                if 'действует' in agreement_status.lower() or 'подписан' in agreement_status.lower():
                    updated_full_agreement_status_list.append(agreement_status)

            updated_status_df = df.loc[df['current_agreement_status'].isin(updated_full_agreement_status_list)]

            df = updated_status_df
            df_temp = df.groupby(['agreement_type', 'year', 'month', 'month_first_date'], as_index=False).agg(
                {'payment_amount': 'sum'})
            df = df_temp

        url_db = os.environ["SQLALCHEMY_DATABASE_URI"]
        engine = sqlalchemy.create_engine(url_db)
        # создаем таблицу agreement_type
        try:
            if_exists = 'replace'
            with engine.connect() as con:
                df.to_sql(
                    name="agreement_type",
                    con=con,
                    # chunksize=1000,
                    # method='multi',
                    index=False,
                    if_exists=if_exists
                )
            output.append('таблица agreement_type создана')
        except Exception as e:
            output.append(f'таблица agreement_type не создана {e}')

        ##################################################################################################

        ############################### СОЗДАНИЕ ТАБЛИЦЫ ДЛЯ ГРАФИКА ПО leasing_product##########
        # готовим таблицу по 'Д_ЛизинговыйПродукт': 'leasing_product
        with engine.connect() as con:

            query = 'SELECT current_agreement_status, leasing_product, year, month, month_first_date, SUM(payment_amount)  FROM "leasing_temp_DB" GROUP BY current_agreement_status, leasing_product, year, month ,month_first_date;'
            df = pd.read_sql(query, con)
            df[['leasing_product']].apply(lambda x: x.astype('category'))
            df['month_first_date'] = pd.to_datetime(df['month_first_date'])
            # удаляем строки, в которых нет leasing_product
            df['leasing_product'].fillna('delete', inplace=True)
            df = df.loc[~df['leasing_product'].isin(['delete', ''])]


            df['year'] = df['year'].astype('int32')
            df['month'] = df['month'].astype('int32')
            df.rename(columns={
                'sum': 'payment_amount'
            }, inplace=True)

            # удаляем ненужные статусы
            full_agreement_status_list = list(df['current_agreement_status'].unique())
            # оставляем только нужные статусы договоров
            updated_full_agreement_status_list = []
            for agreement_status in full_agreement_status_list:
                if 'действует' in agreement_status.lower() or 'подписан' in agreement_status.lower():
                    updated_full_agreement_status_list.append(agreement_status)

            updated_status_df = df.loc[df['current_agreement_status'].isin(updated_full_agreement_status_list)]

            df = updated_status_df
            df_temp = df.groupby(['leasing_product','year','month', 'month_first_date'], as_index=False).agg(
                {'payment_amount': 'sum'})
            df = df_temp

        url_db = os.environ["SQLALCHEMY_DATABASE_URI"]
        engine = sqlalchemy.create_engine(url_db)
        # создаем таблицу leasing_product
        try:
            if_exists = 'replace'
            with engine.connect() as con:
                df.to_sql(
                    name="leasing_product",
                    con=con,
                    # chunksize=1000,
                    # method='multi',
                    index=False,
                    if_exists=if_exists
                )
            output.append('таблица leasing_product создана')
        except Exception as e:
            output.append(f'таблица leasing_product не создана {e}')
        ##################################################################################################

        ############################### СОЗДАНИЕ ТАБЛИЦЫ ДЛЯ ГРАФИКА ПО top group companies##########

        with engine.connect() as con:

            query = 'SELECT current_agreement_status, company_group, year, month, month_first_date, SUM(payment_amount)  FROM "leasing_temp_DB" GROUP BY current_agreement_status, company_group, year, month ,month_first_date;'
            df = pd.read_sql(query, con)
            df[['company_group']].apply(lambda x: x.astype('category'))
            df['month_first_date'] = pd.to_datetime(df['month_first_date'])
            # удаляем строки, в которых нет company_group
            df['company_group'].fillna('delete', inplace=True)
            df = df.loc[~df['company_group'].isin(['delete', ''])]

            df['year'] = df['year'].astype('int32')
            df['month'] = df['month'].astype('int32')
            df.rename(columns={
                'sum': 'payment_amount'
            }, inplace=True)

            # удаляем ненужные статусы
            full_agreement_status_list = list(df['current_agreement_status'].unique())
            # оставляем только нужные статусы договоров
            updated_full_agreement_status_list = []
            for agreement_status in full_agreement_status_list:
                if 'действует' in agreement_status.lower() or 'подписан' in agreement_status.lower():
                    updated_full_agreement_status_list.append(agreement_status)

            updated_status_df = df.loc[df['current_agreement_status'].isin(updated_full_agreement_status_list)]

            df = updated_status_df
            df_temp = df.groupby(['current_agreement_status', 'company_group', 'year', 'month'], as_index=False).agg(
                {'payment_amount': 'sum'})
            df = df_temp

        url_db = os.environ["SQLALCHEMY_DATABASE_URI"]
        engine = sqlalchemy.create_engine(url_db)
        # создаем таблицу company_group
        try:
            if_exists = 'replace'
            with engine.connect() as con:
                df.to_sql(
                    name="company_group",
                    con=con,
                    # chunksize=1000,
                    # method='multi',
                    index=False,
                    if_exists=if_exists
                )
            output.append('таблица company_group создана')
        except Exception as e:
            output.append(f'таблица company_group не создана {e}')
            ##################################################################################################

        ############################### СОЗДАНИЕ ТАБЛИЦЫ ДЛЯ ГРАФИКА ПО top independent companies##########

        with engine.connect() as con:

            query = 'SELECT current_agreement_status, company_group, customer_name, year, month, month_first_date, SUM(payment_amount)  FROM "leasing_temp_DB" GROUP BY current_agreement_status, company_group, customer_name, year, month ,month_first_date;'
            df = pd.read_sql(query, con)
            df[['company_group']].apply(lambda x: x.astype('category'))
            df['month_first_date'] = pd.to_datetime(df['month_first_date'])
            # выделяем строки, в которых есть company_group
            df['company_group'].fillna('independent', inplace=True)
            df = df.loc[df['company_group'].isin(['independent', ''])]


            df['year'] = df['year'].astype('int32')
            df['month'] = df['month'].astype('int32')
            df.rename(columns={
                'sum': 'payment_amount'
            }, inplace=True)

            # удаляем ненужные статусы
            full_agreement_status_list = list(df['current_agreement_status'].unique())
            # оставляем только нужные статусы договоров
            updated_full_agreement_status_list = []
            for agreement_status in full_agreement_status_list:
                if 'действует' in agreement_status.lower() or 'подписан' in agreement_status.lower():
                    updated_full_agreement_status_list.append(agreement_status)

            updated_status_df = df.loc[df['current_agreement_status'].isin(updated_full_agreement_status_list)]

            df = updated_status_df
            df_temp = df.groupby(['current_agreement_status', 'company_group','customer_name', 'year', 'month'],
                                 as_index=False).agg(
                {'payment_amount': 'sum'})
            df = df_temp

        url_db = os.environ["SQLALCHEMY_DATABASE_URI"]
        engine = sqlalchemy.create_engine(url_db)
        # создаем таблицу independent_company
        try:
            if_exists = 'replace'
            with engine.connect() as con:
                df.to_sql(
                    name="independent_company",
                    con=con,
                    # chunksize=1000,
                    # method='multi',
                    index=False,
                    if_exists=if_exists
                )
            output.append('таблица independent_company создана')
        except Exception as e:
            output.append(f'таблица independent_company не создана {e}')
            ##################################################################################################

        ############################### СОЗДАНИЕ ТАБЛИЦЫ ДЛЯ ГРАФИКА ПО products ##########

        with engine.connect() as con:

            query = 'SELECT current_agreement_status, leasing_product, year, month, SUM(payment_amount)  FROM "leasing_temp_DB" GROUP BY current_agreement_status, leasing_product, year, month;'
            df = pd.read_sql(query, con)
        df[['leasing_product']].apply(lambda x: x.astype('category'))

        # удаляем строки, в которых нет leasing_product
        df['leasing_product'].fillna('delete', inplace=True)
        df = df.loc[~df['leasing_product'].isin(['delete', ''])]

        df['year'] = df['year'].astype('int32')
        df['month'] = df['month'].astype('int32')
        df.rename(columns={
            'sum': 'payment_amount'
        }, inplace=True)

        # удаляем ненужные статусы
        full_agreement_status_list = list(df['current_agreement_status'].unique())
        # оставляем только нужные статусы договоров
        updated_full_agreement_status_list = []
        for agreement_status in full_agreement_status_list:
            if 'действует' in agreement_status.lower() or 'подписан' in agreement_status.lower():
                updated_full_agreement_status_list.append(agreement_status)

        updated_status_df = df.loc[df['current_agreement_status'].isin(updated_full_agreement_status_list)]

        df = updated_status_df
        df_temp = df.groupby(['leasing_product', 'year', 'month'],
                             as_index=False).agg(
            {'payment_amount': 'sum'})
        df = df_temp

        url_db = os.environ["SQLALCHEMY_DATABASE_URI"]
        engine = sqlalchemy.create_engine(url_db)
        # создаем таблицу leasing_product
        try:
            if_exists = 'replace'
            with engine.connect() as con:
                df.to_sql(
                    name="leasing_product",
                    con=con,
                    # chunksize=1000,
                    # method='multi',
                    index=False,
                    if_exists=if_exists
                )
            output.append('таблица leasing_product создана')
        except Exception as e:
            output.append(f'таблица leasing_product не создана {e}')
        ##################################################################################################


        ############################### СОЗДАНИЕ ТАБЛИЦЫ ДЛЯ ГРАФИКА ПО leasing_category_2 Видам взаиморасчетов ##########
        with engine.connect() as con:

            query = 'SELECT current_agreement_status, leasing_category_2, year, month, SUM(payment_amount)  FROM "leasing_temp_DB" GROUP BY current_agreement_status, leasing_category_2, year, month;'
            df = pd.read_sql(query, con)
        df[['leasing_category_2']].apply(lambda x: x.astype('category'))

        # удаляем строки, в которых нет leasing_category_2
        df['leasing_category_2'].fillna('delete', inplace=True)
        df = df.loc[~df['leasing_category_2'].isin(['delete', ''])]

        df['year'] = df['year'].astype('int32')
        df['month'] = df['month'].astype('int32')
        df.rename(columns={
            'sum': 'payment_amount'
        }, inplace=True)

        # удаляем ненужные статусы
        full_agreement_status_list = list(df['current_agreement_status'].unique())
        # оставляем только нужные статусы договоров
        updated_full_agreement_status_list = []
        for agreement_status in full_agreement_status_list:
            if 'действует' in agreement_status.lower() or 'подписан' in agreement_status.lower():
                updated_full_agreement_status_list.append(agreement_status)

        updated_status_df = df.loc[df['current_agreement_status'].isin(updated_full_agreement_status_list)]

        df = updated_status_df
        df_to_bd = df.groupby(['leasing_category_2', 'year', 'month'],
                             as_index=False).agg(
            {'payment_amount': 'sum'})

        df_to_bd.rename(columns={
            'leasing_category_2': 'interpayment_type'
        }, inplace=True)




        url_db = os.environ["SQLALCHEMY_DATABASE_URI"]
        engine = sqlalchemy.create_engine(url_db)
        # создаем таблицу leasing_product
        try:
            if_exists = 'replace'
            with engine.connect() as con:
                df_to_bd.to_sql(
                    name="interpayment_type",
                    con=con,
                    # chunksize=1000,
                    # method='multi',
                    index=False,
                    if_exists=if_exists
                )
            output.append('таблица interpayment_type создана')
        except Exception as e:
            output.append(f'таблица interpayment_type не создана {e}')
            ##################################################################################################

        ############################### СОЗДАНИЕ ТАБЛИЦЫ ДЛЯ ГРАФИКА ПО leasing_object_type Видам предмета лизинга ##########
        with engine.connect() as con:

            query = 'SELECT current_agreement_status, leasing_object_type, year, month, SUM(payment_amount)  FROM "leasing_temp_DB" GROUP BY current_agreement_status, leasing_object_type, year, month;'
            df = pd.read_sql(query, con)
        df[['leasing_object_type']].apply(lambda x: x.astype('category'))

        # удаляем строки, в которых нет leasing_object_type
        df['leasing_object_type'].fillna('delete', inplace=True)
        df = df.loc[~df['leasing_object_type'].isin(['delete', ''])]

        df['year'] = df['year'].astype('int32')
        df['month'] = df['month'].astype('int32')
        df.rename(columns={
            'sum': 'payment_amount'
        }, inplace=True)

        # удаляем ненужные статусы
        full_agreement_status_list = list(df['current_agreement_status'].unique())
        # оставляем только нужные статусы договоров
        updated_full_agreement_status_list = []
        for agreement_status in full_agreement_status_list:
            if 'действует' in agreement_status.lower() or 'подписан' in agreement_status.lower():
                updated_full_agreement_status_list.append(agreement_status)

        updated_status_df = df.loc[df['current_agreement_status'].isin(updated_full_agreement_status_list)]

        df = updated_status_df
        df_to_bd = df.groupby(['leasing_object_type', 'year', 'month'],
                              as_index=False).agg(
            {'payment_amount': 'sum'})



        url_db = os.environ["SQLALCHEMY_DATABASE_URI"]
        engine = sqlalchemy.create_engine(url_db)
        # создаем таблицу leasing_object_type
        try:
            if_exists = 'replace'
            with engine.connect() as con:
                df_to_bd.to_sql(
                    name="leasing_object_type",
                    con=con,
                    # chunksize=1000,
                    # method='multi',
                    index=False,
                    if_exists=if_exists
                )
            output.append('таблица leasing_object_type создана')
        except Exception as e:
            output.append(f'таблица leasing_object_type не создана {e}')
            ##################################################################################################

        ############################### СОЗДАНИЕ ТАБЛИЦЫ ДЛЯ ГРАФИКА ПО leasing_rate##########
        with engine.connect() as con:

            query = 'SELECT current_agreement_status, leasing_product, year, leasing_rate, SUM(payment_amount)  FROM "leasing_temp_DB" GROUP BY current_agreement_status, leasing_product, year, leasing_rate;'
            df = pd.read_sql(query, con)

        # output.append(str(df))
        df[['current_agreement_status']].apply(lambda x: x.astype('category'))
        df[['leasing_product']].apply(lambda x: x.astype('category'))

        # # удаляем строки, в которых нет customer_name
        # df['customer_name'].fillna('delete', inplace=True)
        # df = df.loc[~df['customer_name'].isin(['delete', ''])]
        #
        # # удаляем строки, в которых нет leasing_product
        # df['leasing_product'].fillna('delete', inplace=True)
        # df = df.loc[~df['leasing_product'].isin(['delete', ''])]
        #
        #
        df['year'] = df['year'].astype('int32')
        # df['month'] = df['month'].astype('int32')
        df.rename(columns={
            'sum': 'payment_amount'
        }, inplace=True)
        #
        # удаляем ненужные статусы
        full_agreement_status_list = list(df['current_agreement_status'].unique())
        # оставляем только нужные статусы договоров
        updated_full_agreement_status_list = []
        for agreement_status in full_agreement_status_list:
            if 'действует' in agreement_status.lower() or 'подписан' in agreement_status.lower():
                updated_full_agreement_status_list.append(agreement_status)

        updated_status_df = df.loc[df['current_agreement_status'].isin(updated_full_agreement_status_list)]

        df = updated_status_df
        #
        #
        df_to_bd = df.groupby(['leasing_product','leasing_rate', 'year'],
                              as_index=False).agg(
            {'payment_amount': 'sum'})
        #
        url_db = os.environ["SQLALCHEMY_DATABASE_URI"]
        engine = sqlalchemy.create_engine(url_db)
        # создаем таблицу leasing_rate
        try:
            if_exists = 'replace'
            with engine.connect() as con:
                df_to_bd.to_sql(
                    name="leasing_rate",
                    con=con,
                    # chunksize=1000,
                    # method='multi',
                    index=False,
                    if_exists=if_exists
                )
            output.append('таблица leasing_rate создана')
        except Exception as e:
            output.append(f'таблица leasing_rate не создана {e}')
            ##################################################################################################

    return str(output)