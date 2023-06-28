import os
from sqlalchemy import create_engine
import pandas as pd
import datetime
from dash import dash_table
from dash import html
import re
def rd(x, y=3):
    ''' A classical mathematical rounding by Voznica '''
    m = int('1' + '0' * y)  # multiplier - how many positions to the right
    q = x * m  # shift to the right by multiplier
    c = int(q)  # new number
    i = int((q - c) * 10)  # indicator number on the right
    if i >= 5:
        c += 1
    return c / m


def taken_vs_remain_v2_func(data_input, transhi_i_crediti_block_creditor_select, credit_line_type_select):
    output = 'test'
    taken_vs_remain_v2_func_check_ = ""
    date_record_temp = []

    if data_input == '1с_api':
        url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
        engine = create_engine(url_db, pool_recycle=3600)
        with engine.connect() as con:
            # query = 'SELECT *  FROM "creditDB";'
            query = 'SELECT *  FROM "creditdb_2";'
            df_credit_main = pd.read_sql(query, con)
        # df_credit_main.rename(columns={
        #     'sum': 'amount'
        # }, inplace=True)

        with engine.connect() as con:
            # query = 'SELECT *  FROM "creditDB";'
            query = 'SELECT *  FROM "creditnewdata";'
            df_creditnewdata = pd.read_sql(query, con)


        ########################## ПРИМЕНЕНИЕ ФИЛЬТРОВ ######################################################
        df_credit_main['credit_line_type'] = df_credit_main['credit_line_type'].replace('', 'Не возобновляемая')
        full_credit_line_types = ['Возобновляемая', 'Не возобновляемая']
        credit_line_type_list = full_credit_line_types
        if credit_line_type_select:
            if 'list' in str(type(credit_line_type_select)):
                credit_line_type_list = credit_line_type_select
            else:
                credit_line_type_list = []
                credit_line_type_list.append(credit_line_type_select)

        df_credit_main = df_credit_main.loc[df_credit_main['credit_line_type'].isin(credit_line_type_list)]

        # Получаем полный список банков, если в селекте кредиторов пусто
        full_creditor_list = list(df_credit_main['creditor'].unique())

        creditor_list = full_creditor_list
        if transhi_i_crediti_block_creditor_select:
            if 'list' in str(type(transhi_i_crediti_block_creditor_select)):
                creditor_list = transhi_i_crediti_block_creditor_select
            else:
                creditor_list = []
                creditor_list.append(transhi_i_crediti_block_creditor_select)

        df_credit_main = df_credit_main.loc[df_credit_main['creditor'].isin(creditor_list)]


        df_creditnewdata = df_creditnewdata.loc[df_creditnewdata['credit_line_type'].isin(credit_line_type_list)]


        df_creditnewdata = df_creditnewdata.loc[df_creditnewdata['creditor'].isin(creditor_list)]

        ########################## КОНЕЦ ПРИМЕНЕНИЯ ФИЛЬТРОВ ######################################################


        # Прописываем дату начала контракта в оба df
        df_credit_main = df_credit_main.loc[df_credit_main['agreement_code'] == 'Кредиты']
        # получаем список договоров
        agreement_list = list(df_credit_main['contract_title'].unique())
        for agreement in agreement_list:
            agreement_df = df_credit_main.loc[df_credit_main['contract_title']==agreement]
            contract_title_text = agreement_df.iloc[0]['contract_title']
            # получаем первую запись, когда по договору был первый транш.
            agreement_df.sort_values(['credit_tranch_date'], inplace=True, ignore_index=True)
            try:
                credit_agreement_first_date = agreement_df.iloc[0, agreement_df.columns.get_loc("credit_tranch_date")]
            except:
                credit_agreement_first_date = datetime.datetime(datetime.datetime.now().year, 1,1).date()

                # получаем дату начала действия договора, извлекая ее из текста
            try:
                date_record = re.search("[0-9]{1,2}.[0-9]{1,2}.[0-9]{4}",
                                        contract_title_text).group()
                credit_agreement_first_date = datetime.datetime.strptime(date_record, '%d.%m.%Y')
            except Exception as e:
                # date_record_temp.append(e)
                pass
            credit_agreement_first_date = credit_agreement_first_date.date()

            df_credit_main.loc[df_credit_main['contract_title']==agreement, ['credit_agreement_first_date']] = credit_agreement_first_date



        # cоздаем массив из ежедневных дат от начала выплаты траншей до конца текущего года

        # получаем первую дату транша

        df_credit_main.sort_values(['credit_tranch_date'], inplace=True, ignore_index=True)
        transh_first_date = df_credit_main.iloc[0, df_credit_main.columns.get_loc("credit_agreement_first_date")]

        # год даты первого транша:
        transh_first_date_year = transh_first_date.year
        # 1 января года первого транша
        transh_first_date_year_first_date = datetime.datetime(transh_first_date_year, 1, 1)

        current_year = datetime.datetime.now().year
        current_year_first_date = datetime.datetime(current_year, 1, 1)
        current_year_last_date = datetime.datetime(current_year+1, 1, 1)


        df_result_list = []
        temp_date = transh_first_date_year_first_date
        while temp_date <= current_year_last_date:
            temp_dict = {}
            temp_dict['datetime'] = temp_date
            temp_dict['date'] = temp_date.date()
            # temp_dict['creditor'] = ""
            # temp_dict['contract_title'] = ""
            temp_dict['tranch_volume'] = 0
            temp_dict['total_credit_volume'] = 0
            temp_dict['credit_limit'] = 0
            temp_dict['payment'] = 0
            temp_dict['payment_cumulative'] = 0
            temp_dict['tranch_cumulative'] = 0
            temp_dict['credit_allowance_cumulative'] = 0
            temp_dict['credit_limit'] = 0


            df_result_list.append(temp_dict)
            temp_date = temp_date + datetime.timedelta(days=1)

        df_tranch_data = pd.DataFrame(df_result_list)
        # итерируемся по типам линий кредита раздельно для каждой рассчитывая лимиты
        for credit_line_type_ in credit_line_type_list:
            df_credit_main = df_credit_main.loc[df_credit_main['credit_line_type'] == credit_line_type_]

            df_filtered = df_credit_main
            df_filtered_2 = df_filtered.loc[df_filtered['agreement_code'] == 'Кредиты']
            for row in df_filtered_2.itertuples():
                # creditor = getattr(row, 'creditor')
                # contract_title = getattr(row, 'contract_title')
                payment = getattr(row, 'amount')
                payment_datetime = getattr(row, 'date')
                payment_date = payment_datetime.date()
                # текущее значение в payment в df_tranch_data:
                current_payment_value_df_row = df_tranch_data.loc[df_tranch_data['date'] == payment_date]['payment']
                # прибавляем текущее к payment
                updated_payment_value = current_payment_value_df_row + payment
                # переписываем значение payment в df_tranch_data
                df_tranch_data.loc[df_tranch_data['date'] == payment_date, ['payment']] = updated_payment_value


            # получаем список договоров
            agreement_list = list(df_filtered['contract_title'].unique())

            total_credits_volume = 0
            df_filtered = df_filtered.copy()
            df_filtered['tranch_id'] = df_filtered['credit_tranch_date'].astype(str) + "_" + df_filtered['contract_title']

            for contract_name in agreement_list:
                temp_df = df_filtered.loc[df_filtered['contract_title'] == contract_name]

                temp_df = temp_df.copy()
                temp_df.sort_values(['credit_tranch_date'], inplace=True, ignore_index=True)

                # получаем первую запись, когда по договору был первый транш.
                credit_transh_first_date = temp_df.iloc[0, temp_df.columns.get_loc("credit_tranch_date")]


                # получаем список траншей в выборке по договору
                tranch_list_in_contract = list(temp_df['tranch_id'].unique())
                # внутри выборки по договору итерируемся по траншам
                for tranch in tranch_list_in_contract:
                    temp_tranch_df = temp_df.loc[temp_df['tranch_id'] == tranch]
                    # дата транша
                    tranch_date = temp_tranch_df.iloc[0, temp_tranch_df.columns.get_loc("credit_tranch_date")]
                    tranch_id_ = tranch
                    creditor = temp_tranch_df.iloc[0, temp_tranch_df.columns.get_loc("creditor")]
                    tranch_volume = temp_tranch_df.iloc[0, temp_tranch_df.columns.get_loc("credit_amount")]
                    total_credit_volume = temp_tranch_df.iloc[
                        0, temp_tranch_df.columns.get_loc("credit_agreement_total_volume")]

                    # Обновляем данные в df_tranch_data
                    current_tranch_volume_value = df_tranch_data.loc[df_tranch_data['date'] == tranch_date.date(), ['tranch_volume']]
                    updated_tranch_volume_value = current_tranch_volume_value + tranch_volume
                    df_tranch_data.loc[df_tranch_data['date'] == tranch_date.date(), ['tranch_volume']] = updated_tranch_volume_value
                    df_tranch_data.loc[df_tranch_data['date'] == tranch_date.date(), ['total_credit_volume']] = total_credit_volume

            # придется еще раз итерироваться для построения лимитов по каждому договору
            for contract_name in agreement_list:
                temp_df = df_filtered.loc[df_filtered['contract_title'] == contract_name]

                # значение общей суммы кредитого лимита
                credit_volume_by_contract = temp_df.iloc[0, temp_df.columns.get_loc("credit_agreement_total_volume")]

                try:
                    credit_line_type = temp_df.iloc[0, temp_df.columns.get_loc("credit_line_type")]
                except Exception as e:
                    date_record_temp.append(str(e))

                credit_agreement_first_date = temp_df.iloc[0, temp_df.columns.get_loc("credit_agreement_first_date")]

                credit_agreement_last_date = temp_df.iloc[0, temp_df.columns.get_loc("limitdeadline")]

                current_total_credit_volume_value = df_tranch_data.loc[df_tranch_data['date'] == credit_agreement_first_date, ['total_credit_volume']]

                updated_total_credit_volume_value = current_total_credit_volume_value + credit_volume_by_contract
                df_tranch_data.loc[df_tranch_data['date'] == credit_agreement_first_date, ['total_credit_volume']] = updated_total_credit_volume_value

                df_tranch_data['temp_payment_cumulative'] = df_tranch_data['payment'].cumsum()
                df_tranch_data['payment_cumulative'] = df_tranch_data['payment_cumulative'] + df_tranch_data['temp_payment_cumulative']

                df_tranch_data['temp_tranch_cumulative'] = df_tranch_data['tranch_volume'].cumsum()
                df_tranch_data['tranch_cumulative'] = df_tranch_data['tranch_cumulative'] + df_tranch_data[
                    'temp_tranch_cumulative']

                df_tranch_data['temp_credit_allowance_cumulative'] =df_tranch_data['total_credit_volume'].cumsum()
                df_tranch_data['credit_allowance_cumulative'] = df_tranch_data['credit_allowance_cumulative'] + df_tranch_data[
                'temp_credit_allowance_cumulative']

                if credit_line_type_ == 'Возобновляемая':
                    # df_tranch_data.loc[df_tranch_data['contract_title']==contract_name, ['credit_limit']] = df_tranch_data.loc[df_tranch_data['contract_title']==contract_name, ['credit_limit']] + df_tranch_data.loc[df_tranch_data['contract_title']==contract_name, ['credit_allowance_cumulative']] - df_tranch_data.loc[df_tranch_data['contract_title']==contract_name, ['tranch_cumulative']] + df_tranch_data.loc[df_tranch_data['contract_title']==contract_name, ['payment_cumulative']]
                    # df_tranch_data.loc[df_tranch_data['contract_title'] == contract_name, ['credit_limit']] = 12
                    temp_df_indexes = temp_df.index.values
                    # date_record_temp.append(str(temp_df_indexes))
                    df_tranch_data.iloc[temp_df_indexes]['credit_limit'] = 12





            # if credit_line_type == 'Возобновляемая':
            #     # создаем колонку с кумулятивным payment
            #     df_tranch_data['payment_until_today'] = df_tranch_data.apply(
            #         lambda x: x['payment'] if (x['datetime'] <= datetime.datetime.now()) else 0, axis=1)
            #     df_tranch_data['payment_cumulative_restored'] = df_tranch_data['payment_until_today'].cumsum()
            #
            #     # получаем колонку с накопительным итогом траншей
            #     df_tranch_data['tranch_cumulative_restored'] = df_tranch_data['tranch_volume'].cumsum()
            #
            #     # получаем колонку с накопительным итогом максимальных значений
            #     df_tranch_data['credit_allowance_cumulative_restored'] = df_tranch_data['total_credit_volume'].cumsum()
            #
            #
            #     df_tranch_data['credit_limit_restored'] = df_tranch_data['credit_allowance_cumulative_restored']-df_tranch_data['tranch_cumulative_restored']+df_tranch_data['payment_cumulative_restored']
            #
            #     # получаем индексы строк в которых тип = 'Не возобновляемая'
            #
            #
            # elif credit_line_type == 'Не возобновляемая':
            #     # создаем колонку с кумулятивным payment
            #     df_tranch_data['payment_until_today'] = df_tranch_data.apply(
            #         lambda x: x['payment'] if (x['datetime'] <= datetime.datetime.now()) else 0, axis=1)
            #     df_tranch_data['payment_cumulative_non_restored'] = df_tranch_data['payment_until_today'].cumsum()
            #
            #     # получаем колонку с накопительным итогом траншей
            #     df_tranch_data['tranch_cumulative_non_restored'] = df_tranch_data['tranch_volume'].cumsum()
            #
            #     # получаем колонку с накопительным итогом максимальных значений
            #     df_tranch_data['credit_allowance_cumulative_non_restored'] = df_tranch_data['total_credit_volume'].cumsum()
            #     df_tranch_data['credit_limit_non_restored'] = df_tranch_data['credit_allowance_cumulative_non_restored'] - df_tranch_data['tranch_cumulative_non_restored']
            #     # df_tranch_data['credit_limit_restored'] = 0

        data = df_tranch_data.to_dict('records')
        # data = df_credit_main.to_dict('records')

        credit_datatable = dash_table.DataTable(data=data, )
        taken_vs_remain_v2_func_check_ = html.Div(
            children=[
                str(date_record_temp),
                credit_datatable
            ]
        )


    return output, taken_vs_remain_v2_func_check_