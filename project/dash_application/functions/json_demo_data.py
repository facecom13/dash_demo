from pathlib import Path
import pandas as pd
import requests
def json_data_df(input_data_type):
    project_folder = Path(__file__).resolve().parent.parent.parent
    datafiles_path = str(project_folder) + '/datafiles'
    json_credit_demo_data = datafiles_path + '/df_data/credit_demo_data.json'

    df = pd.read_json(json_credit_demo_data, encoding='utf-8')

    if input_data_type == 'json_demo':
        project_folder = Path(__file__).resolve().parent.parent.parent
        datafiles_path = str(project_folder) + '/datafiles'
        json_credit_demo_data = datafiles_path + '/df_data/credit_demo_data.json'

        df = pd.read_json(json_credit_demo_data, encoding='utf-8')
    elif input_data_type == 'json_demo_api':
        response = requests.get('http://51.250.13.192/test_api')
        if response.status_code == 200:
            demo_rest_api_json = response.json()
            df = pd.DataFrame(demo_rest_api_json)

    # присваиваем идентификатор траншу кредита
    df['transh_id'] = df['Кредитор'] +"_" + df['ДатаТраншаКредита']

    df.rename(columns={
        'ОбщаяСуммаДоговора': 'credit_agreement_total_volume',
        'СуммаТраншаКредита': 'credit_volume',
        'ДатаТраншаКредита': 'credit_tranch_date',
        'ВидПлатежа': 'agreement_code',
        'Кредитор': 'creditor',
        'Договор': 'credit_contract',
        'Дата': 'date',
        'ЗначениеПлатежа': 'amount',
        'Ставка': 'credit_annual_rate'

    },
        inplace=True)
    df['credit_agreement_total_volume'] = df['credit_agreement_total_volume'].str.replace(r'\u00A0', '', regex=True)
    df['credit_agreement_total_volume'] = df['credit_agreement_total_volume'].str.replace(',', '.')
    df['credit_agreement_total_volume'] = df['credit_agreement_total_volume'].astype('float')

    df['credit_volume'] = df['credit_volume'].str.replace(r'\u00A0', '', regex=True)
    df['credit_volume'] = df['credit_volume'].str.replace(',', '.')
    df['credit_volume'] = df['credit_volume'].astype('float')

    df['credit_tranch_date'] = pd.to_datetime(df['credit_tranch_date'], format='%d.%m.%Y %H:%M:%S') #11.08.2022 17:26:27
    df['tranch_year'] = df['credit_tranch_date'].dt.year

    df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y %H:%M:%S')
    df['year'] = df['date'].dt.year
    df['quarter'] = df['date'].dt.quarter

    df['amount'] = df['amount'].str.replace(r'\u00A0', '', regex=True)
    df['amount'] = df['amount'].str.replace(',', '.')
    df['amount'] = df['amount'].astype('float')


    df['credit_annual_rate'] = df['credit_annual_rate'].str.replace(r'\u00A0', '', regex=True)
    df['credit_annual_rate'] = df['credit_annual_rate'].str.replace(',', '.')
    df['credit_annual_rate'] = df['credit_annual_rate'].astype('float')


    df.to_csv(datafiles_path + '/df_data/json_demo_data.csv')
    # print(df.info())
    df['credit_amount'] = df['credit_volume']

    return df

# json_data_df()