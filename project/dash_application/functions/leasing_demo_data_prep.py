from pathlib import Path
import pandas as pd
import json
import dash_application.functions.leasing_data as leasing_data
import os
import sqlalchemy
import random
def leasing_demo_data_func():
    try:
        project_folder = Path(__file__).resolve().parent.parent.parent
        datafiles_path = str(project_folder) + '/datafiles'
        json_leasing_demo_data_path = datafiles_path + '/leasing_data/leasing_data.json'
        with open(json_leasing_demo_data_path, encoding='utf-8-sig') as f:
            data = json.load(f)

        # print(json_leasing_demo_data_path)
        # df = pd.read_json(data[0], encoding='utf-8')
        df = pd.DataFrame(data)
        # print(df.info())
        df.rename(columns={
            'ДатаГрафика': 'date',
            'ГруппаКомпаний': 'company_group',
            'Контрагент': 'customer_name',
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
        df['company_group'] = ""
        # заполняем company_group рандомными значениями
        list_of_company_group= ['Полюс', 'Эконива', 'Мираторг', 'Сбертехнологии']
        total_number_of_records = int(len(df))
        requared_number_of_records = int(total_number_of_records*0.3)
        randomlist = random.sample(range(0, total_number_of_records-1), requared_number_of_records)
        i=0
        for row in df.itertuples():
            if i in randomlist:
                record_index = getattr(row, 'Index')
                df.iloc[record_index, df.columns.get_loc("company_group")] = random.choice(list_of_company_group)
            i=i+1

        df = df.loc[:,
             ['date', 'month', 'year','company_group', 'customer_name', 'current_agreement_status', 'payment_amount']]

        # raw_data = leasing_data.leasing_data
        # data_leasing = raw_data['soap:Envelope']['soap:Body']['m:ДоговораЛизингаСводныеДанныеГДАППоМесяцамResponse'][
        #         'm:return']['#text']


        # data_leasing = str(data)
        #
        # data_2 = data_leasing.replace('"', "'")
        # data_3 = data_2.replace("'", '"')
        # data_4 = data_3.replace('\\"', "")
        # data_5 = data_4.replace('\\xa0', '')
        # print(data_5)
        # data_json = json.loads(data_5)
        # print(data_json)
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
        #
        project_folder = Path(__file__).resolve().parent.parent.parent
        db_dir = str(project_folder) + '/database'
        url = 'sqlite:///' + os.path.join(db_dir, 'datab.db')
        # url_db = os.environ["SQLALCHEMY_DATABASE_URI"]

        engine = sqlalchemy.create_engine(url)


        df.to_sql('leasingdemoDB', con=engine, if_exists='replace')
        output_text = "data in leasingdemoDB"
    except Exception as e:
        output_text = f"error: {e}"
        print(output_text)
    return output_text



# leasing_demo_data_func()