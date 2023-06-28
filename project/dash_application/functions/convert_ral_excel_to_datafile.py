import pandas as pd
from pathlib import Path
import numpy as np

def convert_ral_excel_credit():
    project_folder = Path(__file__).resolve().parent.parent.parent
    datafiles_path = str(project_folder) + '/datafiles'
    original_excel_path = datafiles_path + '/df_data/data.xlsx'
    df_leasing_exc = pd.read_excel(original_excel_path, sheet_name='Кредитный портфель')
    # print(df_leasing_exc.info(verbose=True))
    columns_data_index_list = []
    index_col = 15
    while index_col < 90:
        columns_data_index_list.append(index_col)
        index_col = index_col + 1
    # получаем имена заголовков колонок с датами
    payment_data_df = df_leasing_exc.iloc[:, columns_data_index_list]
    payment_data_column_list = list(payment_data_df.columns)

    # итерируемся по выборке из экселя
    temp_df_list = []
    i=0
    for index, row in df_leasing_exc.iterrows():
        credit_volume = row['Сумма транша кредита']
        credit_agreement_total_volume = row['Общая сумма договора']
        credit_tranch_date = row['Дата транша кредита']
        agreement_title = row['Вид договора']

        i=i+1
        transh_id = i
        for column_header in payment_data_column_list:
            temp_dict = {}
            temp_dict['credit_volume'] = credit_volume
            temp_dict['credit_agreement_total_volume'] = credit_agreement_total_volume
            temp_dict['credit_tranch_date'] = credit_tranch_date
            temp_dict['agreement_code'] = row["ВИД"]
            temp_dict['creditor'] = row['Кредитор']
            temp_dict['credit_contract'] = row['Вид договора']
            temp_dict['date'] = column_header
            temp_dict['transh_id'] = transh_id
            temp_dict['contract_title'] = agreement_title
            temp_df_list.append(temp_dict)
    temp_df = pd.DataFrame(temp_df_list)
    temp_df['credit_amount'] = np.random.randint(58832493, 844988093, size=len(temp_df))
    temp_df['credit_annual_rate'] = np.random.uniform(7,18, size=len(temp_df))
    temp_df['amount'] = np.random.randint(20000, 2000000, size=len(temp_df))

    temp_df['date'] = pd.to_datetime(temp_df['date'], format='%Y-%m-%d')
    temp_df['credit_tranch_date'] = pd.to_datetime(temp_df['credit_tranch_date'], format='%d.%m.%Y %H:%M:%S')

    temp_df['tranch_year'] = temp_df['credit_tranch_date'].dt.year
    # temp_df['date'] = pd.to_datetime(temp_df['date'], format='%d.%m.%Y %H:%M:%S')
    temp_df['year'] = temp_df['date'].dt.year
    temp_df['quarter'] = temp_df['date'].dt.quarter
    temp_df['month_first_date'] = (
            temp_df['date'].dt.floor('d') + pd.offsets.MonthEnd(0) - pd.offsets.MonthBegin(1))

    csv_file_path = datafiles_path + '/df_data/csv_credit_file.csv'
    temp_df.to_csv(csv_file_path)

# convert_ral_excel_credit()

def convert_ral_excel():
    project_folder = Path(__file__).resolve().parent.parent.parent
    datafiles_path = str(project_folder) + '/datafiles'
    original_excel_path = datafiles_path + '/df_data/data.xlsx'
    df_leasing_exc = pd.read_excel(original_excel_path)
    # print(df_leasing_exc.columns)
    # итерируемся по рядам и по колонкам.

    result_df_list = []
    # общее количество колонок
    total_columns_qty = len(list(df_leasing_exc.columns))

    columns_data_index_list = []
    index_col = 23
    while index_col < total_columns_qty:
        columns_data_index_list.append(index_col)
        index_col = index_col+1

    # получаем имена заголовков колонок с датами
    payment_data_df = df_leasing_exc.iloc[:, columns_data_index_list]
    payment_data_column_list = list(payment_data_df.columns)


    # итерируемся по выборке из экселя
    for index, row in df_leasing_exc.iterrows():
        for column_header in payment_data_column_list:
            temp_dict = {}
            agreement_code = row["Код договора (АКИС)"]
            temp_dict['agreement_code'] = agreement_code
            agreement_status = row['Статус ДЛ (в периоде отчета)']
            temp_dict['agreement_status'] = agreement_status
            agreement_type = row['Вид договора упр. учета (РАЛ)']
            temp_dict['agreement_type'] = agreement_type
            payment_value = row[column_header]
            temp_dict['date'] = column_header
            temp_dict['payment_value'] = payment_value
            temp_dict['amount'] = payment_value
            result_df_list.append(temp_dict)
    rebuilded_df = pd.DataFrame(result_df_list)
    csv_rebuild_file = datafiles_path + '/df_data/csv_rebuild_file.csv'
    rebuilded_df.to_csv(csv_rebuild_file)

    # получаем группировку для построения графика
    rebuilded_df_groupped = rebuilded_df.groupby(['date', 'agreement_status'], as_index=False).agg({'payment_value': 'sum'})
    rebuilded_df_groupped.sort_values(by="date", inplace=True)
    # добавляем колонку с рандомными значениями
    rebuilded_df_groupped['amount'] = np.random.randint(20000,2000000, size=len(rebuilded_df_groupped))
    csv_rebuild_groupped_file = datafiles_path + '/df_data/csv_rebuild_groupped_file.csv'
    rebuilded_df_groupped.to_csv(csv_rebuild_groupped_file)
    # print(rebuilded_df_groupped)
    return rebuilded_df_groupped

# convert_ral_excel()
def convert_ral_excel_2():
    # project_folder = Path(__file__).resolve().parent.parent.parent
    # datafiles_path = str(project_folder) + '/datafiles'
    # csv_rebuild_groupped_file_path = datafiles_path + '/df_data/csv_rebuild_groupped_file.csv'
    # csv_rebuild_groupped = pd.read_csv(csv_rebuild_groupped_file_path)
    csv_rebuild_groupped_file_path_2 = './datafiles/df_data/csv_rebuild_groupped_file.csv'
    csv_rebuild_groupped = pd.read_csv(csv_rebuild_groupped_file_path_2)


    return csv_rebuild_groupped

def get_credit_type_df():
    credit_type_df_path = './datafiles/df_data/csv_credit_file.csv'
    credit_type_df = pd.read_csv(credit_type_df_path)



    return credit_type_df
