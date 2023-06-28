import dash_bootstrap_components as dbc
from dash import html
import datetime
def credit_tab_taken_tranch_content_func(df, year_filter_list_taken_tranch, taken_tranch_creditor_select_v2):

    year_in_filter = year_filter_list_taken_tranch[0]
    first_day_of_year_selection = datetime.datetime(year_in_filter, 1, 1)
    last_day_of_year_selection = datetime.datetime(year_in_filter+1, 1, 1)
    today = datetime.datetime.now()
    current_year = today.year
    ############# режем df по датам ###################
    df_filtered = df.loc[df['credit_tranch_date']>=first_day_of_year_selection]
    df_filtered = df_filtered.loc[df['credit_tranch_date'] <= last_day_of_year_selection]

    if len(df_filtered) == 0:
        credit_tab_taken_tranch_content = dbc.Card(
            [
                dbc.CardHeader("Выбранные транши"),
                dbc.CardBody(
                    [
                        html.P("Нет данных для расчета")
                    ])
                ])
        return credit_tab_taken_tranch_content

    # Получаем полный список банков, если в селекте кредиторов пусто
    full_creditor_list = list(df_filtered['creditor'].unique())

    creditor_list = full_creditor_list
    if taken_tranch_creditor_select_v2:
        if 'list' in str(type(taken_tranch_creditor_select_v2)):
            creditor_list = taken_tranch_creditor_select_v2
        else:
            creditor_list = []
            creditor_list.append(taken_tranch_creditor_select_v2)


    df = df_filtered.loc[df['creditor'].isin(creditor_list)]

    if len(df) >0:
        # сумма полученных кредитов
        # список transh_id
        transh_id_list = list(df['transh_id'].unique())
        bank_tranch_volume = 0
        for transh_id in transh_id_list:
            temp_df = df.loc[df['transh_id']==transh_id]
            credit_tranch_volume = temp_df['credit_volume'].max()
            bank_tranch_volume = bank_tranch_volume + credit_tranch_volume


        # credit_agreement_total_volume = df['credit_agreement_total_volume'].max()

        # credit_volume_used = bank_tranch_volume/credit_agreement_total_volume *100

        # credit_volume_used = round(credit_volume_used)

        bank_tranch_volume = round(bank_tranch_volume)
        bank_tranch_volume = f"{bank_tranch_volume:,}".replace(',', ' ')
        # credit_agreement_total_volume = f"{credit_agreement_total_volume:,}".replace(',', ' ')

        credit_tab_taken_tranch_content = dbc.Card(
        [
            # dbc.CardHeader("Выбранные транши"),
            dbc.CardBody(
                [
                    html.H4(f"Выбрано в {year_filter_list_taken_tranch[0]}:",
                            # className="card-title",

                            className='custom_H4'
                            ),
                    # html.P(f"на {today.date()}"),
                    html.H5(bank_tranch_volume,
                            # className="card-title"
                            className="custom_H5"
                            ),
                    # html.P(f"{credit_volume_used}% из {credit_agreement_total_volume}", className="card-text"),
                ]
            ),
            # dbc.CardFooter("This is the footer"),
        ],
            # style={"width": "18rem"},
        )


    else:
        credit_tab_taken_tranch_content = dbc.Card(
            [
                dbc.CardHeader("Выбранные транши"),
                dbc.CardBody(
                    [
                        html.H4(f"Выбрано в {year_filter_list_taken_tranch[0]}:",
                                # className="card-title",

                                className='custom_H4'
                                ),
                        # html.H5(bank_tranch_volume,
                        #         # className="card-title"
                        #         className="custom_H5"
                        #         ),
                        html.P(f"Нет данных", className="card-text"),
                    ]
                ),
                # dbc.CardFooter("This is the footer"),
            ],
            # style={"width": "18rem"},
        )

    return credit_tab_taken_tranch_content