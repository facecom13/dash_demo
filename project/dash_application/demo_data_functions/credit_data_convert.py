import pandas as pd
from pathlib import Path
import sqlalchemy
import numpy as np
import os
def credit_data_convert(reload_leasing_table):
    output = 'test'
    if reload_leasing_table:
        project_folder = Path(__file__).resolve().parent.parent.parent
        creditdb_2_file = str(project_folder) + '/creditdb_2.csv'

        credit_df_raw = pd.read_csv(creditdb_2_file, parse_dates=True)
        credit_df_raw['credit_tranch_date'] = pd.to_datetime(credit_df_raw['credit_tranch_date'])
        credit_df_raw['date'] = pd.to_datetime(credit_df_raw['date'])
        credit_df_raw['limitdeadline'] = pd.to_datetime(credit_df_raw['limitdeadline'])
        credit_df_raw['ral_credit_transh_getting_deadline'] = pd.to_datetime(credit_df_raw['ral_credit_transh_getting_deadline'])
        credit_df_raw['month_first_date'] = pd.to_datetime(credit_df_raw['month_first_date'])
        credit_df_raw['record_datetime'] = pd.to_datetime(credit_df_raw['record_datetime'])

        credit_df_raw['amount'] = credit_df_raw['amount'] / 88

        # меняем названия банков
        # текущий список банков
        rename_bank_dict = {}
        bank_list = list(credit_df_raw['creditor'].unique())
        i=1
        for current_bank in bank_list:
            new_bank_name = f'Банк {i}'
            rename_bank_dict[current_bank] = new_bank_name
            i = i+1
        # print(bank_list)
        # rename_bank_dict = {
        #     'БАНК УРАЛСИБ ПАО': 'Сбербанк',
        #     'ПАО БАНК ЗЕНИТ':'Райфазенбанк',
        #     'СМП БАНК АО': 'ВТБ',
        #     'ПРОМСВЯЗЬБАНК ПАО': 'СвязьБанк',
        #     'ФК ОТКРЫТИЕ ПАО БАНК': 'Почта банк',
        #     'НКО АО НРД': 'Банк регионов',
        #     'АБ РОССИЯ АО': 'Владивостокбанк'
        # }

        credit_df_raw['new_creditor'] = credit_df_raw['creditor'].map(rename_bank_dict)

        credit_df_raw.pop('creditor')

        credit_df_raw.rename(columns={
            'new_creditor': 'creditor'
        }, inplace=True)


        # меняем содержимое в поле Кредитный договор
        # ищем пустые строки и заполняем их
        credit_df_raw['contract_title_temp'] = credit_df_raw['contract_title']
        credit_df_raw['contract_title_temp'].fillna("test", inplace=True)
        credit_df_raw['contract_title_temp'] = credit_df_raw['contract_title_temp'].replace('', 'test', regex=True)

        credit_df_raw_temp = credit_df_raw.loc[credit_df_raw['contract_title_temp']!="test"]


        rename_dict = {}
        list_of_contract_title = list(credit_df_raw_temp['contract_title_temp'])
        i = 1
        for item in list_of_contract_title:
            new_name = f'Договор № {i}'
            rename_dict[item] = new_name
            i = i + 1


        credit_df_raw['contract_title_temp'] = credit_df_raw['contract_title'].map(rename_dict)
        credit_df_raw.pop('contract_title')

        credit_df_raw.rename(columns={
            'contract_title_temp': 'contract_title'
        }, inplace=True)

        # меняем содержимое в поле credit_contract
        # ищем пустые строки и заполняем их
        credit_df_raw['credit_contract_temp'] = credit_df_raw['credit_contract']
        credit_df_raw['credit_contract_temp'].fillna("test", inplace=True)
        credit_df_raw['credit_contract_temp'] = credit_df_raw['credit_contract_temp'].replace('', 'test', regex=True)

        credit_df_raw_temp = credit_df_raw.loc[credit_df_raw['credit_contract_temp'] != "test"]

        rename_dict = {}
        list_of_contract_title = list(credit_df_raw_temp['credit_contract_temp'])
        i = 1
        for item in list_of_contract_title:
            new_name = f'Договор № {i}'
            rename_dict[item] = new_name
            i = i + 1

        credit_df_raw['credit_contract_temp'] = credit_df_raw['credit_contract'].map(rename_dict)
        credit_df_raw.pop('credit_contract')
        credit_df_raw.rename(columns={
            'credit_contract_temp': 'credit_contract'
        }, inplace=True)






        try:
            if_exists = 'replace'

            url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
            engine = sqlalchemy.create_engine(url_db)
            with engine.connect() as con:
                credit_df_raw.to_sql(
                    name='creditdb_2',
                    con=con,
                    # chunksize=1000,
                    # method='multi',
                    index=False,
                    if_exists=if_exists
                )
            output = 'credit updated'
        except Exception as e:
            # status_text = f"не получилось создать таблицу creditdb_3: {e}"
            # status = ''
            # return status_text
            pass
        ################# готовим таблицу retail ###############################
        df_retail = credit_df_raw

        # создаем поле Клиент
        rename_dict = {}
        df_retail['customer_name_temp'] = df_retail['creditor']
        list_of_creditor_name = list(df_retail['customer_name_temp'])
        i = 1
        for item in list_of_creditor_name:
            new_name = f'Контрагент № {i}'
            rename_dict[item] = new_name
            i = i + 1

        df_retail['customer_name_temp'] = df_retail['creditor'].map(rename_dict)
        df_retail.pop('creditor')
        df_retail.rename(columns={
            'customer_name_temp': 'customer_name'
        }, inplace=True)

        rename_dict = {
            "Кредиты": "Холдинги",
            "Проценты": "Розница"
        }
        df_retail['agreement_code_temp'] = df_retail['agreement_code']
        df_retail['agreement_code_temp'] = df_retail['agreement_code'].map(rename_dict)
        df_retail.pop('agreement_code')
        df_retail.rename(columns={
            'agreement_code_temp': 'agreement_code'
        }, inplace=True)



        # Создаем поле с менеджерами
        list_of_managers = ['Носов А.А', 'Николаев К.С.', 'Осипов Р.В.', 'Пахомов В.Н.', 'Самойлова Р.А', 'Бобылева В.Е', 'Кузнецова Е.В']

        qty_of_managers = len(list_of_managers)
        df_retail['manager'] = np.random.choice(list_of_managers, len(df_retail))




        try:
            if_exists = 'replace'
            url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
            engine = sqlalchemy.create_engine(url_db)
            with engine.connect() as con:
                df_retail.to_sql(
                    name='retail',
                    con=con,
                    # chunksize=1000,
                    # method='multi',
                    index=False,
                    if_exists=if_exists
                )
            output = 'credit updated'
        except Exception as e:
            status_text = f"не получилось создать таблицу retail: {e}"
            # status = ''
            return status_text





        # print(df_retail)




    return output



# credit_data_convert(1)