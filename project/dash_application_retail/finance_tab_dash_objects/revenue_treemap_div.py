import datetime
from dash import html, dcc
import plotly.graph_objects as go
import pandas as pd
import os
from sqlalchemy import create_engine
import dash_application_retail.colors as colors_file

def revenue_treemap_div_func(retail_customer_select):
    output = 'credit_treemap_div_content'
    url_db = os.environ["SQLALCHEMY_DATABASE_URI_PSYCORG2"]
    engine = create_engine(url_db, pool_recycle=3600)
    with engine.connect() as con:
        query = 'SELECT *  FROM "retail";'
        df = pd.read_sql(query, con)




    df['year'] = df['year'].astype(float)
    df['year'] = df['year'].astype('int')
    # режем df по фильтрам

    # фильтр по кредитору ###########################################################################
    customer_name_full_list = list(df['customer_name'].unique())
    customer_name_filter = customer_name_full_list
    if retail_customer_select:
        if 'list' in str(type(retail_customer_select)):
            customer_name_filter = retail_customer_select
        else:
            customer_name_filter = list(retail_customer_select)

    # режем выборку по кредитору
    df = df.loc[df['customer_name'].isin(customer_name_filter)]

    #####################################################################################################

    # фильтр по credit_contract ##########################################################################
    # credit_contract_full_list = list(df['credit_contract'].unique())
    # credit_contract_filter = credit_contract_full_list
    # if credit_contract_select:
    #     if 'list' in str(type(credit_contract_select)):
    #         credit_contract_filter = credit_contract_select
    #     else:
    #         credit_contract_filter = list(credit_contract_select)
    #
    # # режем выборку по credit_contract
    # df = df.loc[df['credit_contract'].isin(credit_contract_filter)]
    #####################################################################################################

    # фильтр по годам ###########################################################################
    # year_full_list = list(df['year'].unique())
    # year_filter = year_full_list
    # if credit_year_select:
    #     if 'list' in str(type(credit_year_select)):
    #         year_filter = credit_year_select
    #     else:
    #         year_filter = [credit_year_select]
    #
    # year_filter_int_list = []
    # for year in year_filter:
    #     year = int(year)
    #     if year >= int(datetime.datetime.now().year):
    #         year_filter_int_list.append(year)
    #
    # # режем выборку по годам
    # df = df.loc[df['year'].isin(year_filter_int_list)]
    #####################################################################################################

    # фильтр по кварталам ###########################################################################
    # quarter_full_list = list(df['quarter'].unique())
    # quarter_filter = quarter_full_list
    # if credit_tab_quarter_select:
    #     if 'list' in str(type(credit_tab_quarter_select)):
    #         quarter_filter = credit_tab_quarter_select
    #     else:
    #         quarter_filter = [credit_tab_quarter_select]
    #
    # quarter_filter_int_list = []
    # for quarter in quarter_filter:
    #     quarter = int(quarter)
    #     quarter_filter_int_list.append(quarter)
    #
    # # режем выборку по кварталам
    # df = df.loc[df['quarter'].isin(quarter_filter_int_list)]
    #####################################################################################################

    # фильтр по месяцам ###########################################################################
    # month_full_list = [1,2,3,4,5,6,7,8,9,10,11,12]
    # month_filter = month_full_list
    # if credit_tab_month_select:
    #     if 'list' in str(type(credit_tab_month_select)):
    #         month_filter = credit_tab_month_select
    #     else:
    #         month_filter = [credit_tab_month_select]
    #
    # month_filter_int_list = []
    # for month in month_filter:
    #     month = int(month)
    #     month_filter_int_list.append(month)
    #
    # df['date_2'] = pd.to_datetime(df['date'])
    # if "int" in str(df['date'].dtype):
    #     df['date_2'] = pd.to_datetime(df['date'], unit='ms')
    # df['month'] = df['date_2'].dt.month
    # # режем выборку по месяцам
    # df = df.loc[df['month'].isin(month_filter_int_list)]
    #####################################################################################################



    today = datetime.datetime.now()

    try:
        df = df.loc[df['date'] >= today]
    except:
        df = df.loc[df['date'] >= today.date()]

    df_groupped = df.groupby(['agreement_code', 'customer_name'], as_index=False).agg(
        {'amount': 'sum'})
    labels = ['Выручка']
    parents = ['']
    values = [0]
    text = [] # суммарное значение всех выплат, попавших в выборку

    # суммарное значение всех выплат, попавших в выборку
    total_payment_value = df['amount'].sum()
    total_payment_value = round(total_payment_value/1000000, 3)
    total_payment_value_str = str(total_payment_value) + " млн.руб"
    text.append(total_payment_value_str)
    # print('total_payment_value: ',total_payment_value)

    # Получаем список категорий из колонки agreement_code
    agreement_code_list = list(df_groupped['agreement_code'].unique())
    # добавляем эти категории первым уровнем в родительский корень
    for agreement_code_list_item in agreement_code_list:
        labels.append(agreement_code_list_item)
        parents.append('Выручка')
        # получаем значения для категорий Кредиты и проценты
        agreement_code_list_item_df = df.loc[df['agreement_code']==agreement_code_list_item]
        agreement_code_temp_value = agreement_code_list_item_df['amount'].sum()

        values.append(0)

        agreement_code_payment_value = round(agreement_code_temp_value / 1000000, 3)
        agreement_code_payment_value = '{:.1f}'.format(agreement_code_payment_value)
        agreement_code_payment_value_str = str(agreement_code_payment_value) + " млн.руб"
        text.append(agreement_code_payment_value_str)

        # группируем результат по полю customer_name
        agreement_code_groupped_df = agreement_code_list_item_df.groupby(['customer_name'], as_index=False).agg(
            {'amount': 'sum'})
        # итерируемся по полученному df
        for row in agreement_code_groupped_df.itertuples():
            amount = getattr(row, 'amount')
            amount = round(amount/1000000, 3)

            amount_str = '{:.1f}'.format(amount)
            amount_str = str(amount_str) + " млн.руб"

            customer_name_payment_value_str = amount_str

            # добавляем в списки treemap значения
            if agreement_code_list_item == 'Розница':
                customer_name = getattr(row, 'customer_name') + " "
            else:
                customer_name = getattr(row, 'customer_name')
            labels.append(customer_name)
            values.append(amount)
            text.append(customer_name_payment_value_str)
            parents.append(agreement_code_list_item)


    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        text = text,
        values=values,
        textinfo="label+text+percent parent",
        hoverinfo="label+text+percent parent",
        root={"color": "#f6f8f7"}
    ))

    first_main_color = colors_file.colors_dict[0]
    second_main_color = colors_file.colors_dict[1]

    fig.update_layout(
        margin=dict(t=5, l=5, r=5, b=25),
        treemapcolorway=[first_main_color, second_main_color],
    )

    # получаем первую дату в выборке
    df.sort_values(['date'], inplace=True)
    first_date = df.iloc[0, df.columns.get_loc("date")]
    first_date = today
    last_date = df.iloc[-1, df.columns.get_loc("date")]


    output = html.Div(
        children=[
            dcc.Graph(figure = fig, config = {'displayModeBar': False})
        ]
    )

    # output = 'credit_treemap_div_content'
    return output, first_date, last_date