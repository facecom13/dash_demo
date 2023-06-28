import datetime
import dash_application.dash_objects.initial_values as initial_values
import pandas as pd

def credit_avrate_download_func(df, creditor_select, credit_contract_select, credit_year_select, credit_tab_quarter_select, credit_tab_month_select):
    ave_rate_df = pd.DataFrame()
    df['year'] = df['year'].astype(float)
    df['year'] = df['year'].astype('int')
    # режем df по фильтрам

    # фильтр по кредитору ###########################################################################
    creditor_full_list = list(df['creditor'].unique())
    creditor_filter = creditor_full_list
    if creditor_select:
        if 'list' in str(type(creditor_select)):
            creditor_filter = creditor_select
        else:
            creditor_filter = list(creditor_select)

    # режем выборку по кредитору
    df = df.loc[df['creditor'].isin(creditor_filter)]

    #####################################################################################################

    # фильтр по credit_contract ##########################################################################
    credit_contract_full_list = list(df['credit_contract'].unique())
    credit_contract_filter = credit_contract_full_list
    if credit_contract_select:
        if 'list' in str(type(credit_contract_select)):
            credit_contract_filter = credit_contract_select
        else:
            credit_contract_filter = list(credit_contract_select)

    # режем выборку по credit_contract
    df = df.loc[df['credit_contract'].isin(credit_contract_filter)]
    #####################################################################################################

    # фильтр по годам ###########################################################################
    year_full_list = list(df['year'].unique())
    year_filter = year_full_list
    if credit_year_select:
        if 'list' in str(type(credit_year_select)):
            year_filter = credit_year_select
        else:
            year_filter = [credit_year_select]

    year_filter_int_list = []
    for year in year_filter:
        year = int(year)
        if year >= int(datetime.datetime.now().year):
            year_filter_int_list.append(year)

    # режем выборку по годам
    df = df.loc[df['year'].isin(year_filter_int_list)]
    #####################################################################################################

    # фильтр по кварталам ###########################################################################
    quarter_full_list = list(df['quarter'].unique())
    quarter_filter = quarter_full_list
    if credit_tab_quarter_select:
        if 'list' in str(type(credit_tab_quarter_select)):
            quarter_filter = credit_tab_quarter_select
        else:
            quarter_filter = [credit_tab_quarter_select]

    quarter_filter_int_list = []
    for quarter in quarter_filter:
        quarter = int(quarter)
        quarter_filter_int_list.append(quarter)

    # режем выборку по кварталам
    df = df.loc[df['quarter'].isin(quarter_filter_int_list)]
    #####################################################################################################

    # фильтр по месяцам ###########################################################################
    month_full_list = [1,2,3,4,5,6,7,8,9,10,11,12]
    month_filter = month_full_list
    if credit_tab_month_select:
        if 'list' in str(type(credit_tab_month_select)):
            month_filter = credit_tab_month_select
        else:
            month_filter = [credit_tab_month_select]

    month_filter_int_list = []
    for month in month_filter:
        month = int(month)
        month_filter_int_list.append(month)

    df['date_2'] = pd.to_datetime(df['date'])
    if "int" in str(df['date'].dtype):
        df['date_2'] = pd.to_datetime(df['date'], unit='ms')
    df['month'] = df['date_2'].dt.month
    # режем выборку по месяцам
    df = df.loc[df['month'].isin(month_filter_int_list)]
    #####################################################################################################

    today = datetime.datetime.now()

    try:
        df = df.loc[df['date'] >= today]
    except:
        df = df.loc[df['date'] >= today.date()]

    # print('len_df: ', len(df))
    if len(df) > 0:

        # необходимо посчитать текущий остаток обязательств
        # это сумма по полю amount в будущее

        df = df.loc[:,
             ['date', 'creditor', 'credit_tranch_date', 'credit_annual_rate', 'credit_amount', 'agreement_code',
              'amount']]
        # список траншей в работе
        df['tranch_ids'] = df['credit_tranch_date'].astype(str) + "_" + df['creditor'].astype(str)

        creditor_list = list(df['creditor'].unique())
        # колонка с размером годовой суммы процентов
        df = df.copy()
        df['credit_percent_annual_amount'] = df['credit_annual_rate'] / 100 * df['credit_amount']

        # сумма процентов
        percent_sum = df['credit_percent_annual_amount'].sum()
        credit_sum = df['credit_amount'].sum()
        percent_value = percent_sum / credit_sum

        # data = df.to_dict('records')
        # credit_datatable = dash_table.DataTable(
        #
        #     data=data,)

        x_credit_rate = []
        y_credit_rate = []
        result_list = []
        total_credit_amount = df['credit_amount'].sum()
        total_percent_amount = df['credit_percent_annual_amount'].sum()

        for creditor in creditor_list:

            # получаем выборку по банку
            creditor_temp_df = df.loc[df['creditor'] == creditor]

            # стоимость остатка от кредитов
            creditor_temp_df = creditor_temp_df.loc[creditor_temp_df['agreement_code'] == 'Кредиты']

            # получаем список размера ставок, попавших в выборку
            creditor_rates_list = list(creditor_temp_df['credit_annual_rate'].unique())

            for rate in creditor_rates_list:
                temp_dict = {}
                temp_dict['creditor'] = creditor
                temp_dict['rate'] = rate

                creditor_rate_temp_df = creditor_temp_df.loc[creditor_temp_df['credit_annual_rate'] == rate]

                credit_remainings = creditor_rate_temp_df['amount'].sum()
                """ credit_remainings - сумма всего что есть в поле amount в будущем """

                creditor_rate_temp_df = creditor_rate_temp_df.copy()
                creditor_rate_temp_df['percent_amount'] = creditor_rate_temp_df['amount'] * rate / 100
                percent_amount = creditor_rate_temp_df['percent_amount'].sum()

                temp_dict['credit_remainings'] = credit_remainings
                temp_dict['percent_amount'] = percent_amount
                result_list.append(temp_dict)

        ave_rate_df = pd.DataFrame(result_list)

    credit_excel_rename_dict = initial_values.credit_excel_rename_dict
    ave_rate_df.rename(columns=credit_excel_rename_dict, inplace=True)

    return ave_rate_df