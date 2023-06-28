import datetime
from dash import html

def rd(x, y=3):
    ''' A classical mathematical rounding by Voznica '''
    m = int('1' + '0' * y)  # multiplier - how many positions to the right
    q = x * m  # shift to the right by multiplier
    c = int(q)  # new number
    i = int((q - c) * 10)  # indicator number on the right
    if i >= 5:
        c += 1
    return c / m




def credit_taken_by_today_content_func(df, transhi_i_crediti_block_creditor_select, credit_line_type_select):
    today = datetime.datetime.now()
    df['credit_line_type'] = df['credit_line_type'].replace('', 'Не возобновляемая')
    full_credit_line_types = ['Возобновляемая', 'Не возобновляемая']
    credit_line_type_list = full_credit_line_types
    if credit_line_type_select:
        if 'list' in str(type(credit_line_type_select)):
            credit_line_type_list = credit_line_type_select
        else:
            credit_line_type_list = []
            credit_line_type_list.append(credit_line_type_select)

    df = df.loc[df['credit_line_type'].isin(credit_line_type_list)]






    # Получаем полный список банков, если в селекте кредиторов пусто
    full_creditor_list = list(df['creditor'].unique())

    creditor_list = full_creditor_list
    if transhi_i_crediti_block_creditor_select:
        if 'list' in str(type(transhi_i_crediti_block_creditor_select)):
            creditor_list = transhi_i_crediti_block_creditor_select
        else:
            creditor_list = []
            creditor_list.append(transhi_i_crediti_block_creditor_select)

    df = df.loc[df['creditor'].isin(creditor_list)]

    if len(df) >0:
        # сумма полученных кредитов
        # список transh_id
        transh_id_list = list(df['transh_id'].unique())
        bank_tranch_volume = 0
        bank_tranch_volume_by_start_of_year = 0
        # print(df.info())
        current_year = datetime.datetime.now().year
        for transh_id in transh_id_list:
            temp_df = df.loc[df['transh_id']==transh_id]
            tranch_date = temp_df.iloc[0, df.columns.get_loc("credit_tranch_date")]
            credit_tranch_volume = temp_df['credit_volume'].max()
            bank_tranch_volume = bank_tranch_volume + credit_tranch_volume
            if tranch_date <= datetime.datetime(current_year, 1, 1):
                bank_tranch_volume_by_start_of_year = bank_tranch_volume_by_start_of_year + credit_tranch_volume
            else:
                continue

        # значение на 1 января 2023 года
        bank_tranch_volume = bank_tranch_volume - bank_tranch_volume_by_start_of_year
        # bank_tranch_volume = round(bank_tranch_volume/1000000000,3)
        bank_tranch_volume = format(rd(bank_tranch_volume / 1000000000), '.3f')

        bank_tranch_volume_output = html.P(bank_tranch_volume)

    else:
        bank_tranch_volume_output = html.P("-")

    return bank_tranch_volume_output