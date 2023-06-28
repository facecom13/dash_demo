import pandas as pd

def credit_by_bank_download_excel_data_df_func(data):
    df = pd.read_json(data)
    try:
        df.rename(columns={
            'ОбщаяСуммаДоговора': 'credit_agreement_total_volume',
            'СуммаТраншаКредита': 'credit_volume',
            'ДатаТраншаКредита': 'credit_tranch_date',
            'ВидПлатежа': 'agreement_code',
            'Кредитор': 'creditor',
            'Договор': 'credit_contract',
            'ВидДоговора': 'contract_title',
            'Дата': 'date',
            'ЗначениеПлатежа': 'amount',
            'Ставка': 'credit_annual_rate'

        }, inplace=True)
    except:
        pass
    try:
        df['credit_tranch_date'] = pd.to_datetime(df['credit_tranch_date'], format="%d.%m.%Y %H:%M:%S")
    except:
        pass

    if "int" in str(df['credit_tranch_date'].dtype):
        df['credit_tranch_date'] = pd.to_datetime(df['credit_tranch_date'], unit='ms')
    else:
        df['credit_tranch_date'] = pd.to_datetime(df['credit_tranch_date'])

    if "int" in str(df['date'].dtype):
        df['date'] = pd.to_datetime(df['date'], unit='ms')
    else:
        df['date'] = pd.to_datetime(df['date'])

    ######## первая дата в выборке  #######
    df.sort_values(['date'], inplace=True, ignore_index=True)
    first_date = df.iloc[0, df.columns.get_loc("date")]
    # message = str(first_date)
    ##########################################

    df['year'] = df['date'].dt.year
    df['year_dt'] = pd.to_datetime(df['year'], format='%Y')

    df['quarter'] = df['date'].dt.quarter
    df['month'] = df['date'].dt.month
    df['month_first_date'] = (df['date'].dt.floor('d') + pd.offsets.MonthEnd(0) - pd.offsets.MonthBegin(1))



    data_ = {
        "Данные": ["Это заглушка"],

    }

    # load data into a DataFrame object:
    # df = pd.DataFrame(data_)

    return df

