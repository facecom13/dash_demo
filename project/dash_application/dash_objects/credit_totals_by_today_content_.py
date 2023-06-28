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


def credit_totals_by_today_content_func(df, transhi_i_crediti_block_creditor_select, credit_line_type_select):
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

    # Пусть Кредитный портфель - это сумма всех выплат в будущем со статусом Кредиты
    # Поэтому сначала режем от сегодня - в будущее
    df = df.loc[df['date']>=today]
    # режем по типу выплаты
    df = df.loc[df['agreement_code']=='Кредиты']
    # суммируем все что есть в поле Amount

    if len(df)>0:

        total_remaining_credit_amount = df['amount'].sum()
        # total_remaining_credit_amount = round(total_remaining_credit_amount / 1000000000, 3)
        total_remaining_credit_amount = format(rd(total_remaining_credit_amount/ 1000000000), '.3f')

        output = html.P(total_remaining_credit_amount)

    else:
        output = html.P("-")

    return output