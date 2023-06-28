from pathlib import Path
import pandas as pd
import json


def leasing_data_parser_func(data_input):
    leasing_data = ""
    if data_input == 'demo':
        project_folder = Path(__file__).resolve().parent.parent.parent
        data_file_path = str(project_folder) + '/datafiles/leasing_data/leasing_demo.json'
        # print(data_file_path)
        with open(data_file_path, "r") as readfile:
            # print(readfile)
            leasing_demo_data_json = json.load(readfile)
            leasing_data = leasing_demo_data_json


    data_credit = str(leasing_data)
    data_2 = data_credit.replace('"', "'")
    data_3 = data_2.replace("'", '"')
    data_4 = data_3.replace('\\"', "")
    data_5 = data_4.replace('\\xa0', '')
    data_json = json.loads(data_5)
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
    df = df.loc[:, ['date','month', 'year', 'current_agreement_status', 'payment_amount']]



    return df

